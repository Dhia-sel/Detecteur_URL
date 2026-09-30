# Training Data Sources

## Current Model

`phiusiil.csv` is the local PhiUSIIL dataset used by `phishing_model.py`. UCI
documents 235,795 labeled web URLs/pages (134,850 legitimate, 100,945 phishing)
and licenses the dataset under CC BY 4.0. Its raw URL column supports the
HTTP(S) hierarchical model; its documentation does not claim labeled coverage
for `data:`, nested redirect chains, or opaque URI schemes.

- Dataset: https://archive.ics.uci.edu/dataset/967/phiusiil+phishing+url+dataset
- Download: https://archive.ics.uci.edu/static/public/967/phiusiil+phishing+url+dataset.zip
- Citation: Prasad and Chandra, PhiUSIIL Phishing URL (Website), UCI, 2024.
- License: CC BY 4.0; retain attribution when redistributing derived datasets.

## Other Sources Reviewed

| Source | Useful coverage | Use decision |
| --- | --- | --- |
| PhishTank online-valid feed | Community-verified phishing web URLs; positive class only | Current terms link to Cisco's EULA. Do not ingest into training until permitted use, derivative models, and redistribution are confirmed. |
| OpenPhish Community Feed | Limited, current phishing web URLs; positive class only | Terms limit use to personal/academic research that does not support organizational business and prohibit sharing/derivative works without written permission. Not included. |
| URLhaus | Malware-distribution HTTP(S) URLs, not phishing; explicitly excludes redirect-only sites | Current terms prohibit using its data to develop, train, fine-tune, or validate AI models. Do not use for model training. |
| ISCX-URL-2016 | Historical web URLs with multiple threat classes | Publisher download requires registration/contact; a reusable license and redirect/opaque URI coverage were not verified. Not included. |

No verified public dataset was found that supplies both benign and malicious,
ground-truth examples for `data:` payloads, nested redirect URLs, and opaque URI
schemes such as `mailto:` or `javascript:`. Existing unit-test examples are
fixtures, not a representative or independently labeled training corpus. Do
not convert them into claimed training data.

## Import Format For Future Type-Specific Training

Use `typed_urls_template.csv` as the input format for a separately licensed,
reviewed corpus. Keep payloads inert: the project parses strings and must never
open or execute submitted URLs while importing or validating them.

Required columns:

- `url_type`: `embedded`, `nested`, or `opaque`.
- `url`: the exact observed URI string.
- `label`: `0` for benign, `1` for malicious.
- `source`: source name and dataset version or a documented annotation batch.
- `verified_at`: ISO-8601 label verification date.

Validate a candidate file offline before training:

```powershell
python ML/validate_typed_dataset.py ML/typed_urls_template.csv --minimum-per-class 100
```

The command exits non-zero when a type is missing, a declared type does not
match the project classifier, duplicate strings occur, labels are invalid, or
any required class has too few samples. The default threshold is only a minimum
ingestion guard, not a production-quality claim. Before deployment, collect at
least 1,000 examples per class and type where feasible, use domain/source- and
time-separated validation, review false positives, and calibrate each model on
an independent validation set. Never report a model as trained for a type
until those checks pass.