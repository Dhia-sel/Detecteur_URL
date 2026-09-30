"""Validate a reviewed, licensed URI dataset without opening its URLs."""

import argparse
import csv
from collections import Counter
from pathlib import Path

from App.Core.classifier import URLClassifier
from App.Core.normalizer import URLNormalizer


SUPPORTED_TYPES = {"embedded", "nested", "opaque"}
CLASSIFICATION_NAMES = {
    "embarqué": "embedded",
    "imbriqué": "nested",
    "hiérarchique": "hierarchical",
    "opaque": "opaque",
}
REQUIRED_COLUMNS = {"url_type", "url", "label", "source", "verified_at"}


def validate_dataset(path, minimum_per_class=100):
    path = Path(path)
    rows = []
    errors = []
    seen = set()
    counts = Counter()

    with path.open("r", encoding="utf-8-sig", newline="") as dataset_file:
        reader = csv.DictReader(dataset_file)
        columns = set(reader.fieldnames or ())
        missing = REQUIRED_COLUMNS - columns
        if missing:
            return {"rows": 0, "counts": {}, "errors": [
                f"Missing required columns: {', '.join(sorted(missing))}"
            ]}

        for line_number, row in enumerate(reader, start=2):
            url_type = (row.get("url_type") or "").strip().lower()
            url = (row.get("url") or "").strip()
            label_text = (row.get("label") or "").strip()
            source = (row.get("source") or "").strip()
            verified_at = (row.get("verified_at") or "").strip()

            if url_type not in SUPPORTED_TYPES:
                errors.append(f"Line {line_number}: unsupported url_type {url_type!r}.")
                continue
            if not url or not source or not verified_at:
                errors.append(f"Line {line_number}: url, source, and verified_at are required.")
                continue
            if label_text not in {"0", "1"}:
                errors.append(f"Line {line_number}: label must be 0 (benign) or 1 (malicious).")
                continue

            try:
                normalized = URLNormalizer(url).normalize_url()
                detected = CLASSIFICATION_NAMES.get(URLClassifier(normalized).classify())
            except (TypeError, ValueError) as error:
                errors.append(f"Line {line_number}: cannot classify URL: {error}")
                continue

            if detected != url_type:
                errors.append(
                    f"Line {line_number}: declared {url_type!r}, classifier detected {detected!r}."
                )
                continue

            unique_key = (url_type, url)
            if unique_key in seen:
                errors.append(f"Line {line_number}: duplicate URL for type {url_type!r}.")
                continue
            seen.add(unique_key)
            label = int(label_text)
            counts[(url_type, label)] += 1
            rows.append({"url_type": url_type, "url": url, "label": label, "source": source})

    for url_type in sorted(SUPPORTED_TYPES):
        for label in (0, 1):
            count = counts[(url_type, label)]
            if count < minimum_per_class:
                class_name = "benign" if label == 0 else "malicious"
                errors.append(
                    f"{url_type}: needs at least {minimum_per_class} {class_name} rows; found {count}."
                )

    summary = {
        url_type: {
            "benign": counts[(url_type, 0)],
            "malicious": counts[(url_type, 1)],
        }
        for url_type in sorted(SUPPORTED_TYPES)
    }
    return {"rows": len(rows), "counts": summary, "errors": errors}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("dataset", type=Path)
    parser.add_argument("--minimum-per-class", type=int, default=100)
    args = parser.parse_args()
    if args.minimum_per_class < 1:
        parser.error("--minimum-per-class must be at least 1")

    result = validate_dataset(args.dataset, args.minimum_per_class)
    print(f"Accepted rows: {result['rows']}")
    for url_type, counts in result["counts"].items():
        print(f"{url_type}: benign={counts['benign']}, malicious={counts['malicious']}")
    for error in result["errors"]:
        print(f"ERROR: {error}")
    if result["errors"]:
        raise SystemExit(1)
    print("Dataset passed structural checks. This does not establish label quality or license rights.")


if __name__ == "__main__":
    main()