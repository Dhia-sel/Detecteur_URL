import unittest

from ML.phishing_model import extract


class MLFeatureNormalizationTests(unittest.TestCase):
    def test_root_slash_does_not_change_features(self):
        self.assertEqual(
            extract("https://www.bbc.com"),
            extract("https://www.bbc.com/"),
        )

    def test_non_root_trailing_slash_is_preserved(self):
        self.assertNotEqual(
            extract("https://www.bbc.com/news"),
            extract("https://www.bbc.com/news/"),
        )

    def test_www_prefix_does_not_change_features(self):
        self.assertEqual(
            extract("https://stackoverflow.com/"),
            extract("https://www.stackoverflow.com/"),
        )

    def test_credentials_and_port_survive_www_normalization(self):
        self.assertEqual(
            extract("https://user:pass@www.example.com:8443/path"),
            extract("https://user:pass@example.com:8443/path"),
        )


if __name__ == "__main__":
    unittest.main()