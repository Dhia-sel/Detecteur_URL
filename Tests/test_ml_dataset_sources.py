import unittest

import pandas as pd

from ML.phishing_model import _is_hierarchical_web_url, _prepare_labeled_urls


class TrainingDatasetSourceTests(unittest.TestCase):
    def test_legitphish_label_mapping_and_non_web_filter(self):
        source = pd.DataFrame({
            "URL": [
                "https://phishing.example/login",
                "https://safe.example/",
                "data:text/html,<p>x</p>",
                "Offline",
            ],
            "ClassLabel": [0, 1, 0, 0],
        })

        prepared = _prepare_labeled_urls(
            source,
            "URL",
            "ClassLabel",
            phishing_label=0,
            source="LegitPhish V2",
        )

        self.assertEqual(
            dict(zip(prepared.url, prepared.phish)),
            {
                "https://phishing.example/login": 1,
                "https://safe.example": 0,
            },
        )

    def test_nested_url_is_not_used_as_hierarchical_training_example(self):
        self.assertFalse(
            _is_hierarchical_web_url(
                "https://www.facebook.com/l.php?u=http://evil.example/login"
            )
        )

    def test_web_urls_are_accepted_but_embedded_and_opaque_are_rejected(self):
        self.assertTrue(_is_hierarchical_web_url("https://www.example.com/path"))
        self.assertTrue(_is_hierarchical_web_url("https://192.0.2.10/path"))
        self.assertFalse(_is_hierarchical_web_url("mailto:user@example.com"))
        self.assertFalse(_is_hierarchical_web_url("data:text/plain,hello"))


if __name__ == "__main__":
    unittest.main()
