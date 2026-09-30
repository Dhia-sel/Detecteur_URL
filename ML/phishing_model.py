import math
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

import joblib
import pandas as pd
from sklearn.ensemble import HistGradientBoostingClassifier

HERE = Path(__file__).resolve().parent
MODEL_PATH = HERE / "phishing_model.joblib"
DATA_PATH = HERE / "phiusiil.csv"
FEATURE_VERSION = 1
KEYWORDS = ("login", "signin", "verify", "secure", "account", "update", "bank",
            "confirm", "password", "wallet", "webscr", "paypal", "support")
TRUSTED_DOMAINS = {
    "google.com", "google.co.uk", "google.ca", "google.de", "google.fr",
    "microsoft.com", "apple.com", "amazon.com", "github.com", "wikipedia.org",
    "mozilla.org", "cloudflare.com", "example.com",
}


def _entropy(s):
    if not s:
        return 0.0
    return -sum((s.count(c) / len(s)) * math.log2(s.count(c) / len(s)) for c in set(s))


def normalize(url):
    url = url.strip()
    if not re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*://", url):
        url = "https://" + url
    parsed = urlparse(url)
    if parsed.scheme.lower() in {"http", "https"}:
        netloc = parsed.netloc
        userinfo, separator, host_port = netloc.rpartition("@")
        if not separator:
            host_port = netloc
        if host_port.lower().startswith("www."):
            host_port = host_port[4:]
            netloc = f"{userinfo}@{host_port}" if separator else host_port
        path = "" if parsed.path == "/" else parsed.path
        url = parsed._replace(netloc=netloc, path=path).geturl()
    return url


def hostname_of(url):
    try:
        return (urlparse(normalize(url)).hostname or "").lower()
    except ValueError:
        return ""


def extract(url):
    url = normalize(url)
    try:
        p = urlparse(url)
        host = (p.hostname or "").lower()
        has_port = int(p.port is not None)
    except ValueError:
        p, host, has_port = urlparse("https://x"), "", 0
    labels = host.split(".") if host else []
    n = max(len(url), 1)
    letters = sum(c.isalpha() for c in url)
    digits = sum(c.isdigit() for c in url)
    tokens = re.split(r"[^a-zA-Z0-9]+", url)
    low = url.lower()
    return {
        "url_len": len(url), "host_len": len(host), "path_len": len(p.path),
        "query_len": len(p.query),
        "n_dots": url.count("."), "n_hyphen": url.count("-"),
        "n_underscore": url.count("_"), "n_slash": url.count("/"),
        "n_at": url.count("@"), "n_qmark": url.count("?"), "n_eq": url.count("="),
        "n_amp": url.count("&"), "n_percent": url.count("%"), "n_hash": url.count("#"),
        "n_digits": digits, "digit_ratio": digits / n, "letter_ratio": letters / n,
        "special_ratio": (n - letters - digits) / n,
        "is_https": int(p.scheme == "https"),
        "is_ip": int(bool(re.fullmatch(r"\d{1,3}(\.\d{1,3}){3}", host))),
        "has_port": has_port,
        "n_subdomains": max(len(labels) - 2, 0),
        "tld_len": len(labels[-1]) if labels else 0,
        "host_hyphens": host.count("-"),
        "host_digits": sum(c.isdigit() for c in host),
        "has_punycode": int("xn--" in host),
        "path_depth": p.path.count("/"),
        "max_token_len": max((len(t) for t in tokens), default=0),
        "url_entropy": _entropy(url), "host_entropy": _entropy(host),
        "n_keywords": sum(k in low for k in KEYWORDS),
        "has_file_ext": int(bool(re.search(r"\.(php|html?|asp|aspx|exe|zip)$", p.path.lower()))),
    }


def build_matrix(urls):
    return pd.DataFrame([extract(u) for u in urls])


def load_dataset(progress_callback=None):
    if DATA_PATH.exists():
        if progress_callback:
            progress_callback("loading_dataset", "Chargement du dataset PhiUSIIL local.")
        df = pd.read_csv(DATA_PATH)
    else:
        from ucimlrepo import fetch_ucirepo
        if progress_callback:
            progress_callback("downloading_dataset", "Téléchargement du dataset PhiUSIIL depuis UCI.")
        df = fetch_ucirepo(id=967).data.original
        df.to_csv(DATA_PATH, index=False)
    if progress_callback:
        progress_callback("dataset_ready", f"Dataset prêt : {len(df)} lignes récupérées.")
    df.columns = [c.lower() for c in df.columns]
    df = df[["url", "label"]].dropna().drop_duplicates(subset="url")
    df["phish"] = (df["label"] == 0).astype(int)
    return df[["url", "phish"]].reset_index(drop=True)


def make_model():
    return HistGradientBoostingClassifier(
        max_iter=300, learning_rate=0.1, max_depth=8, random_state=42
    )


def _is_trusted_clean_url(url):
    try:
        parsed = urlparse(normalize(url))
        host = (parsed.hostname or "").lower().rstrip(".")
        if (parsed.scheme != "https" or parsed.port not in (None, 443)
                or parsed.username is not None or parsed.password is not None):
            return False
        if not any(host == domain or host.endswith("." + domain) for domain in TRUSTED_DOMAINS):
            return False
        path_and_query = f"{parsed.path}?{parsed.query}".lower()
        if "http" in parsed.query.lower() or re.search(
                r"(?:^|[&;])(url|redirect(?:_url)?|next|target|dest|continue|return)=",
                parsed.query,
                re.IGNORECASE,
        ):
            return False
        return not any(re.search(rf"(?<![a-z0-9]){re.escape(keyword)}(?![a-z0-9])", path_and_query)
                       for keyword in KEYWORDS)
    except ValueError:
        return False


def train(progress_callback=None):
    df = load_dataset(progress_callback)
    X, y = build_matrix(df["url"]), df["phish"]
    if progress_callback:
        progress_callback("training", f"Entraînement du modèle sur {len(df)} URLs.")
    model = make_model().fit(X, y)
    joblib.dump({"model": model, "columns": list(X.columns), "feature_version": FEATURE_VERSION}, MODEL_PATH)
    if progress_callback:
        progress_callback("ready", f"Modèle entraîné et enregistré dans {MODEL_PATH.name}.")
    else:
        print(f"Modèle entraîné sur {len(df)} URLs -> {MODEL_PATH.name}")


_BUNDLE = None


def phishing_percent(url):
    global _BUNDLE
    if _BUNDLE is None:
        if not MODEL_PATH.exists():
            train()
        _BUNDLE = joblib.load(MODEL_PATH)
    features = extract(url)
    if (set(_BUNDLE["columns"]) != set(features)
            or _BUNDLE.get("feature_version") != FEATURE_VERSION):
        train()
        _BUNDLE = joblib.load(MODEL_PATH)
    X = pd.DataFrame([features])[_BUNDLE["columns"]]
    score = float(_BUNDLE["model"].predict_proba(X)[0, 1]) * 100
    if _is_trusted_clean_url(url):
        return min(score, 5.0)
    return score


def verdict(pct):
    return "PHISHING probable" if pct >= 50 else "suspect" if pct >= 20 else "probablement sain"


if __name__ == "__main__":
    args = sys.argv[1:]
    if not args:
        print("Usage: python phishing_model.py train | <URL> [<URL> ...]")
        sys.exit(0)
    if args[0] == "train":
        train()
    else:
        for u in args:
            pct = phishing_percent(u)
            print(f"{pct:5.1f} % phishing  [{verdict(pct)}]  {u}")