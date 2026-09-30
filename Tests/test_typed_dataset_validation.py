import csv
import tempfile
import unittest
from pathlib import Path

from ML.validate_typed_dataset import validate_dataset


class TypedDatasetValidationTests(unittest.TestCase):
    def write_rows(self, rows):
        temporary_directory = tempfile.TemporaryDirectory()
        self.addCleanup(temporary_directory.cleanup)
        dataset_path = Path(temporary_directory.name) / "typed.csv"
        fields = ["url_type", "url", "label", "source", "verified_at"]
        with dataset_path.open("w", encoding="utf-8", newline="") as dataset_file:
            writer = csv.DictWriter(dataset_file, fieldnames=fields)
            writer.writeheader()
            writer.writerows(rows)
        return dataset_path

    def test_requires_both_classes_for_each_uri_type(self):
        rows = [
            {"url_type": "embedded", "url": "data:text/plain,hello", "label": 0, "source": "fixture", "verified_at": "2026-01-01"},
            {"url_type": "embedded", "url": "data:text/html,<script>x</script>", "label": 1, "source": "fixture", "verified_at": "2026-01-01"},
        ]

        result = validate_dataset(self.write_rows(rows), minimum_per_class=1)

        self.assertEqual(result["counts"]["embedded"], {"benign": 1, "malicious": 1})
        self.assertEqual(len(result["errors"]), 4)

    def test_rejects_mismatched_declared_type(self):
        rows = [{
            "url_type": "embedded",
            "url": "https://example.com/",
            "label": 0,
            "source": "fixture",
            "verified_at": "2026-01-01",
        }]

        result = validate_dataset(self.write_rows(rows), minimum_per_class=1)

        self.assertTrue(any("classifier detected 'hierarchical'" in error for error in result["errors"]))

    def test_rejects_duplicate_urls(self):
        row = {"url_type": "opaque", "url": "mailto:a@example.com", "label": 0, "source": "fixture", "verified_at": "2026-01-01"}

        result = validate_dataset(self.write_rows([row, row]), minimum_per_class=1)

        self.assertTrue(any("duplicate URL" in error for error in result["errors"]))


if __name__ == "__main__":
    unittest.main()