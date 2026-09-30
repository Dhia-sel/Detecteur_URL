import unittest

from App.Core.pipeline import URLAnalyzerPipeline
from App.Explaining.formatter import BaseFormatter


class FormatterRegressionTests(unittest.TestCase):
    def test_mime_messages_are_mutually_exclusive(self):
        cases = [
            ({"risky_mime": 0, "is_unknown": 1}, "MIME type is missing or could not be parsed."),
            ({"risky_mime": 1, "is_unknown": 0}, "Uses a risky MIME type (JavaScript, HTML, executable, etc.)."),
            ({"risky_mime": 0, "is_unknown": 0}, "A MIME type is available for classification."),
            ({"risky_mime": 1, "is_unknown": 1}, "Uses a risky MIME type (JavaScript, HTML, executable, etc.)."),
        ]
        for mime_values, expected in cases:
            analyzer_values = {
                "base64": 0,
                "hidden_html": 0,
                "small_payload": 0,
                **mime_values,
            }
            _, comments = BaseFormatter({}, {"behaviour": analyzer_values})._format_analyzer(analyzer_values)
            mime_comments = [comment for comment in comments if "MIME type" in comment]
            with self.subTest(mime_values=mime_values):
                self.assertEqual(mime_comments, [expected])


    def test_data_html_reports_only_risky_mime(self):
        result = URLAnalyzerPipeline("data:text/html,<html></html>").run()

        self.assertTrue(result["success"])
        mime_comments = [
            comment
            for comment in result["report"]["comments"]["behaviour"]
            if "MIME type" in comment
        ]
        self.assertEqual(
            mime_comments,
            ["Uses a risky MIME type (JavaScript, HTML, executable, etc.)."],
        )

    def test_nested_length_ratio_requires_a_disproportionate_value(self):
        from App.Explaining.formatter import _is_hazardous

        self.assertFalse(_is_hazardous("len_ratio", 1.5))
        self.assertFalse(_is_hazardous("len_ratio", 3.0))
        self.assertTrue(_is_hazardous("len_ratio", 3.01))

    def test_script_markup_does_not_get_a_conflicting_code_message(self):
        result = URLAnalyzerPipeline("data:text/html,<script>alert(1)</script>").run()
        comments = result["report"]["comments"]["lexical"]

        self.assertIn(
            "Contains one or more monitored HTML elements.",
            comments,
        )
        self.assertNotIn("No harmful code indicators detected.", comments)

    def test_mailto_is_not_classified_as_a_risky_scheme(self):
        result = URLAnalyzerPipeline("mailto:user@example.com?subject=hello").run()
        behaviour = result["report"]["data"]["behaviour"]
        comments = result["report"]["comments"]["behaviour"]

        self.assertEqual(behaviour["is_risky"], 0)
        self.assertNotIn(
            "Uses a potentially risky scheme (bitcoin, javascript, data, etc.).",
            comments,
        )
