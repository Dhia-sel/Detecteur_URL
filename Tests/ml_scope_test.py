import unittest

from API.routes.scan import _get_ml_result, scan_url
from API.schema.scan_schema import ScanRequest
from App.Core.classifier import URLClassifier
from App.Core.normalizer import URLNormalizer


class MLApplicabilityTests(unittest.TestCase):
    def test_facebook_u_parameter_is_classified_as_nested(self):
        url = "https://www.facebook.com/l.php?u=http://phishing-bank.com/login.php"
        normalized = URLNormalizer(url).normalize_url()

        self.assertEqual(URLClassifier(normalized).classify(), "imbriqué")

    def test_non_hierarchical_types_do_not_receive_ml_probabilities(self):
        cases = {
            "data:text/plain,Hello": "embedded",
            "https://www.google.com/url?url=https%3A%2F%2Fwww.google.com%2F": "nested",
            "mailto:admin@example.com": "opaque",
        }
        for url, url_type in cases.items():
            with self.subTest(url_type=url_type):
                result = _get_ml_result(url, url_type=url_type)
                self.assertEqual(result["status"], "unsupported")
                self.assertIsNone(result["score"])
                self.assertIsNone(result["verdict"])

    def test_supplied_embedded_uri_returns_rule_signal_count(self):
        url = "data:application/x-javascript;base64,ZXZhbChhdG9iKCdhbGVydChkb2N1bWVudC5jb29raWUpJykpOw=="

        result = scan_url(ScanRequest(url=url))

        self.assertEqual(result["ml"]["status"], "unsupported")
        self.assertIsNone(result["ml"]["score"])
        self.assertEqual(result["ml"]["risk_signal_count"], 8)
        self.assertEqual(result["ml"]["risk_signal_total"], 11)
        self.assertEqual(result["ml"]["rule_score_percent"], 72.7)

    def test_all_url_types_return_a_numeric_score(self):
        samples = {
            "hierarchical": "https://www.bbc.com/",
            "embedded": "data:text/plain,Hello%20world",
            "nested": "https://www.facebook.com/l.php?u=http://phishing-bank.com/login.php",
            "opaque": "javascript:alert(1)",
        }
        for expected_type, url in samples.items():
            with self.subTest(url_type=expected_type):
                result = scan_url(ScanRequest(url=url))
                self.assertTrue(result["success"])
                self.assertEqual(result["url_type"], expected_type)
                if expected_type == "hierarchical":
                    self.assertEqual(result["ml"]["status"], "ready")
                    self.assertIsInstance(result["ml"]["score"], (int, float))
                else:
                    self.assertEqual(result["ml"]["status"], "unsupported")
                    self.assertIsNone(result["ml"]["score"])
                    self.assertIsInstance(result["ml"]["rule_score_percent"], (int, float))


if __name__ == "__main__":
    unittest.main()