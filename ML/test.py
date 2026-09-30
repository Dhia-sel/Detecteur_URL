import numpy as np
import pandas as pd
from sklearn.inspection import permutation_importance
from sklearn.metrics import (accuracy_score, confusion_matrix, f1_score,
                             precision_score, recall_score, roc_auc_score)
from sklearn.model_selection import GroupKFold, GroupShuffleSplit, train_test_split

import phishing_model as pm

lines = []


def out(s=""):
    print(s)
    lines.append(s)


def evaluate(title, Xtr, ytr, Xte, yte):
    model = pm.make_model().fit(Xtr, ytr)
    p_tr, p_te = model.predict(Xtr), model.predict(Xte)
    proba = model.predict_proba(Xte)[:, 1]
    tn, fp, fn, tp = confusion_matrix(yte, p_te).ravel()
    out(f"\n=== {title} ===")
    out(f"URLs train / test            : {len(ytr)} / {len(yte)}")
    out(f"Accuracy entraînement        : {accuracy_score(ytr, p_tr):.2%}")
    out(f"Accuracy test                : {accuracy_score(yte, p_te):.2%}")
    out(f"Precision (phishing)         : {precision_score(yte, p_te):.2%}")
    out(f"Recall (phishing détectés)   : {recall_score(yte, p_te):.2%}")
    out(f"F1-score                     : {f1_score(yte, p_te):.2%}")
    out(f"ROC-AUC                      : {roc_auc_score(yte, proba):.4f}")
    out(f"Faux positifs (sain -> alerte): {fp} ({fp / (fp + tn):.2%} des sains)")
    out(f"Faux négatifs (phishing raté) : {fn} ({fn / (fn + tp):.2%} des phishing)")
    out(f"Matrice [[TN FP] [FN TP]]    : [[{tn} {fp}] [{fn} {tp}]]")
    return model


def main():
    df = pm.load_dataset()
    out(f"Dataset : PhiUSIIL | {len(df)} URLs uniques | phishing : {df['phish'].mean():.1%}")
    X, y = pm.build_matrix(df["url"]), df["phish"].to_numpy()
    groups = pd.factorize(pd.Series([pm.hostname_of(u) for u in df["url"]]))[0]
    out(f"Domaines distincts : {groups.max() + 1}")

    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)
    evaluate("Test 1 - split aléatoire 80/20", Xtr, ytr, Xte, yte)

    tr, te = next(GroupShuffleSplit(test_size=0.2, random_state=42).split(X, y, groups))
    model = evaluate("Test 2 - split par domaine (plus réaliste)",
                     X.iloc[tr], y[tr], X.iloc[te], y[te])

    sub = slice(0, 20000)
    imp = pd.Series(
        permutation_importance(model, X.iloc[te][sub], y[te][sub],
                               n_repeats=3, random_state=42).importances_mean,
        index=X.columns).sort_values(ascending=False)
    out("\nTop 8 features (permutation importance, test 2) :")
    out(imp.head(8).round(4).to_string())

    accs = []
    for a, b in GroupKFold(n_splits=5).split(X, y, groups):
        m = pm.make_model().fit(X.iloc[a], y[a])
        accs.append(accuracy_score(y[b], m.predict(X.iloc[b])))
    out("\n=== Test 3 - validation croisée 5-fold par domaine ===")
    out("Accuracy par fold : " + ", ".join(f"{a:.2%}" for a in accs))
    out(f"Moyenne : {np.mean(accs):.2%} (+/- {np.std(accs):.2%})")

    (pm.HERE / "stats_report.txt").write_text("\n".join(lines), encoding="utf-8")
    out("\nRapport écrit dans stats_report.txt")


if __name__ == "__main__":
    main()