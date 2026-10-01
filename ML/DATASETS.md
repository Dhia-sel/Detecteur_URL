# Training Data Sources

## Production HTTP(S) Model

The hierarchical URL model trains on the local PhiUSIIL data plus LegitPhish
V2 when `ML/datasets/legitphish_v2.csv` is present. The loader keeps raw URL
strings, converts labels to `phish=1`, normalizes the root slash and `www.`
consistently with inference, and filters non-HTTP(S), nested, and malformed
records. Identical URLs with conflicting labels are excluded.

Run `python ML/download_training_datasets.py` to download the reviewed Mendeley
CSVs. They are ignored by Git and remain local. After downloading, train with
`python ML/phishing_model.py train`. The saved bundle records its dataset
recipe version and sources, so an older artifact is retrained automatically.

### PhiUSIIL

- UCI describes 235,795 web URL/page records: 134,850 legitimate and 100,945 phishing.
- Raw `URL` plus `label`; label `0` is phishing and `1` legitimate.
- License: CC BY 4.0. Cite Prasad and Chandra (2024), UCI PhiUSIIL.
- [Dataset page](https://archive.ics.uci.edu/dataset/967/phiusiil+phishing+url+dataset) · [CSV ZIP](https://archive.ics.uci.edu/static/public/967/phiusiil+phishing+url+dataset.zip)

### LegitPhish V2

- Mendeley V2 reports 101,219 rows; the published class totals sum to 101,218, and one row has a missing label. The loader drops invalid/missing rows.
- Raw `URL` plus `ClassLabel`; `0` is phishing and `1` legitimate.
- License: CC BY 4.0. Cite Potpelwar, Kulkarni, and Waghmare (2025), LegitPhish Dataset V2.
- [Dataset page](https://data.mendeley.com/datasets/hx4m73v2sf/2) · [CSV](https://data.mendeley.com/public-files/datasets/hx4m73v2sf/files/0ed51e4d-d160-4047-b650-3f0801eea4aa/file_downloaded)

## Benchmarked, Not Included In Production Training

### URL-Phish V2

- V2 (March 2026) reports 116,600 raw URL rows: 100,000 benign (`label=0`) and 16,600 phishing (`label=1`); the URL column is available.
- License: CC BY 4.0. Cite Dam Minh and Tran Cong (2026), URL-Phish V2.
- [Dataset page](https://data.mendeley.com/datasets/65z9twcx3r/2) · [CSV](https://data.mendeley.com/public-files/datasets/65z9twcx3r/files/0e9c55e4-9adb-43f5-8403-1bbd143ebdb6/file_downloaded)
- It is downloaded for reproducible comparison, but not mixed into the production model: the measured grouped-domain merge increased FPR and FNR substantially.

### CompPhish V4

- Mendeley V4 describes 15,358 labeled web URLs (7,204 phishing, 8,154 legitimate), raw HTML, and 70 engineered features. Labels: `0` legitimate, `1` phishing.
- License: CC BY 4.0. Cite Goenka (2026), CompPhish V4.
- [Dataset page and files](https://data.mendeley.com/datasets/fmbs4kp9wz/4). Its HTML archive is about 692 MB and is not downloaded by this project.
- HTML page content is not a dataset of `data:` URIs. Wrapping pages into generated data URIs would be synthetic augmentation, not observed URI data, and is not currently used for training.

### PhishStorm

- Aalto describes 96,018 URLs, balanced 48,009 legitimate / 48,009 phishing; raw URL is in the `domain` column. Labels: `0` legitimate, `1` phishing.
- The Aalto dataset record lists the license as unspecified. It is therefore not downloaded or used for training until reuse rights are clarified.
- [Aalto record and download](https://research.aalto.fi/en/datasets/f49465b2-c68a-4182-9171-075f0ed797d5) · [DOI](https://doi.org/10.24342/f49465b2-c68a-4182-9171-075f0ed797d5)

### Kaggle Phishing URL Features Dataset

- The data card reports 579,920 rows, 74 lexical/DNS/WHOIS features, and labels `0` legitimate / `1` phishing under CC BY 4.0.
- The card describes precomputed features but does not establish that the downloadable table retains raw URLs. This model requires URL strings for its feature extractor, so it is not included unless its schema is verified.
- [Kaggle data card](https://www.kaggle.com/datasets/elifzelik/phishing-url-features-dataset)

## Coverage Of The Four URI Families

Coverage below was measured by running this repository's classifier over the
raw URL columns available in the local snapshots; it is not inferred from the
dataset titles.

| Corpus | Hierarchical HTTP(S) | Nested | Embedded `data:` | Opaque |
| --- | ---: | ---: | ---: | ---: |
| PhiUSIIL local snapshot after model normalization | 235,549 | 246 excluded as nested (all phishing) | 0 | 0 |
| LegitPhish V2 local snapshot after model normalization | 101,206 | 1 excluded as nested (phishing) | 0 | 0 |
| URL-Phish V2 local snapshot after model normalization | 116,495 | 105 excluded as nested (104 phishing, 1 benign) | 0 | 0 |
| CompPhish V4 metadata | Raw web URLs/HTML | Not documented as labeled nested URI data | 0 documented | 0 documented |
| PhishStorm metadata | Raw web URLs | Not documented | 0 documented | 0 documented |
| Kaggle data card | Raw URL column not verified | Not documented | Not documented | Not documented |

LegitPhish improves the hierarchical model, but these snapshots do not supply
balanced supervised data for embedded or opaque URIs. The observed nested
examples are very imbalanced. Those three types continue to receive rule-based
scores; this training change does not claim an ML model for them.

## Validation Results

One fixed `GroupShuffleSplit` evaluation grouped by hostname; the same feature
extractor, classifier settings, and 50% threshold were used for each candidate.
These results compare the datasets, not certify real-world performance.

| Training data | Test URLs | ROC-AUC | Brier | FPR | FNR |
| --- | ---: | ---: | ---: | ---: | ---: |
| PhiUSIIL only | 47,279 | 0.99253 | 0.01455 | 0.67% | 3.12% |
| PhiUSIIL + LegitPhish V2 | 59,244 | 0.99535 | 0.01267 | 0.88% | 2.03% |
| PhiUSIIL + LegitPhish + URL-Phish V2 | 86,637 | 0.97700 | 0.05757 | 4.85% | 12.61% |

The deployed recipe uses PhiUSIIL + LegitPhish: this split improved AUC, Brier,
and false-negative rate with a small false-positive increase. URL-Phish V2 is
kept as a comparison source because its merge degraded metrics. Repeat testing
across source- and time-separated splits before treating these figures as
certification.

## Import Format For Other URI Types

`typed_urls_template.csv` is the format for separately licensed and reviewed
examples of `embedded`, `nested`, and `opaque` URIs. The validator parses strings
offline and never opens or executes submitted URLs.

Required columns: `url_type` (`embedded`, `nested`, or `opaque`), `url`, `label`
(`0` benign / `1` malicious), `source` with version/provenance, and `verified_at`
(ISO-8601).

```powershell
python ML/validate_typed_dataset.py ML/typed_urls_template.csv --minimum-per-class 100
```

This is only a structural minimum, not a production-quality threshold. Aim for
at least 1,000 examples per class and URI type where feasible, split by source,
domain, and time; review false positives and calibrate on an independent test
set. Do not represent unit-test fixtures or generated wrappers as observed data.

## Sources Not Used

PhishTank's current terms link to Cisco's EULA; confirm model-training and
redistribution permissions before use. OpenPhish Community Feed terms limit
use to personal/academic research that does not support organizational business
and prohibit sharing/derivative works without written permission. URLhaus terms
prohibit training, fine-tuning, or validation of AI models. These sources are
not downloaded or used by this project.
