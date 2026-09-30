from .messages import RISK_MESSAGES, FEATURE_MESSAGES


FEATURE_RISK = {
    "is_ip": "high_bad",
    "is_private": "high_bad",
    "abnormal_port": "high_bad",
    "sus_tld": "high_bad",
    "is_ssl": "high_good",
    "len": "high_bad",
    "dots": "high_bad",
    "dashes": "high_bad",
    "special_chars": "high_bad",
    "subdomain_depth": "high_bad",
    "keywords": "high_bad",
    "entropy": "high_bad",
    "digitRatio": "high_bad",
    "has_redirection": "high_bad",
    "has_obfuscation": "high_bad",
    "is_shortened": "high_bad",
    "multi_subdomain": "high_bad",
    "double_slash": "high_bad",
    "semantic_score": "high_bad",
    "code_score": "high_bad",
    "tag_count": "high_bad",
    "pwd_field": "high_bad",
    "symbol_ratio": "high_bad",
    "risky_mime": "high_bad",
    "base64": "high_bad",
    "hidden_html": "high_bad",
    "is_unknown": "high_bad",
    "small_payload": "high_bad",
    "bad_extention": "high_bad",
    "len_ratio": "high_bad",
    "percent_count": "high_bad",
    "equal_count": "high_bad",
    "trusted_wrapper": "high_good",
    "downgrade": "high_bad",
    "is_external": "high_bad",
    "key_standard": "high_good",
    "target_digit": "high_bad",
    "money_signs": "high_bad",
    "dest_len": "high_bad",
    "payload_len": "high_bad",
    "is_risky": "high_bad",
    "dest_count": "high_bad",
    "multi_target": "high_bad",
    "has_options": "high_bad",
    "risky_payload": "high_bad"
}

FEATURE_THRESHOLDS = {
    "len": 75,
    "dots": 3,
    "dashes": 2,
    "special_chars": 3,
    "subdomain_depth": 2,
    "entropy": 3.5,
    "digitRatio": 0.1,
    "len_ratio": 3.0,
    "dest_len": 40,
    "payload_len": 3,
    "percent_count": 2,
    "equal_count": 2,
    "dest_count": 1,
}


def _is_hazardous(feature, value):
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        return False
    if FEATURE_RISK.get(feature, "high_bad") == "high_good":
        return value == 0
    return value > FEATURE_THRESHOLDS.get(feature, 0)


def count_risk_signals(analyses):
    return sum(
        _is_hazardous(feature, value)
        for values in analyses.values()
        for feature, value in values.items()
    )


def calculate_rule_risk_score(analyses):
    evaluated_count = sum(
        isinstance(value, (int, float))
        and not isinstance(value, bool)
        and feature in FEATURE_MESSAGES
        for values in analyses.values()
        for feature, value in values.items()
    )
    signal_count = count_risk_signals(analyses)
    score_percent = round(signal_count / evaluated_count * 100, 1) if evaluated_count else 0.0
    return {
        "risk_signal_count": signal_count,
        "risk_signal_total": evaluated_count,
        "rule_score_percent": score_percent,
    }


class BaseFormatter:
    def __init__(self, parsed_data, analyses):
        self.parsed = parsed_data
        self.analyses = analyses

    def _format_analyzer(self, analyzer_values):
        data = {}
        comments = []
        for sub_key, sub_value in analyzer_values.items():
            data[sub_key] = sub_value
            if sub_value is None:
                continue
            if sub_key in FEATURE_MESSAGES:
                if sub_key == "is_unknown" and analyzer_values.get("risky_mime", 0):
                    continue
                if sub_key == "risky_mime" and sub_value == 0 and "is_unknown" in analyzer_values:
                    continue
                if _is_hazardous(sub_key, sub_value):
                    comments.append(FEATURE_MESSAGES[sub_key]['hazardous'])
                else:
                    comments.append(FEATURE_MESSAGES[sub_key]['safe'])
        return data, comments

    def format_analyzers(self):
        data = {}
        comments = {}
        for analyzer, values in self.analyses.items():
            d, c = self._format_analyzer(values)
            data[analyzer] = d
            comments[analyzer] = c
        return data, comments

    def get_recommendation(self):
        hazardous_count = count_risk_signals(self.analyses)
        if hazardous_count > 5:
            return RISK_MESSAGES["high"]
        elif hazardous_count > 2:
            return RISK_MESSAGES["medium"]
        else:
            return RISK_MESSAGES["low"]

class HierarchicalFormatter(BaseFormatter):
    def __init__(self, parsed_data, analyses):
        super().__init__(parsed_data, analyses)
        self.host = parsed_data.get("auteur", {}).get("le hote", "")
        self.scheme = parsed_data.get("schéma", "")

    def format_report(self):
        data, comments = self.format_analyzers()
        return {
            "url_type": "hierarchical",
            "parsed_url": self.parsed,
            "data": data,
            "comments": comments,
            "recommendation": self.get_recommendation(),
            "specific_insights": f"Host: {self.host}, Scheme: {self.scheme}"
        }

class EmbeddedFormatter(BaseFormatter):
    def __init__(self, parsed_data, analyses):
        super().__init__(parsed_data, analyses)
        self.data_type = parsed_data.get("type_média", "")

    def format_report(self):
        data, comments = self.format_analyzers()
        return {
            "url_type": "embedded",
            "parsed_url": self.parsed,
            "data": data,
            "comments": comments,
            "recommendation": self.get_recommendation(),
            "specific_insights": f"Embedded data type: {self.data_type}"
        }

class NestedFormatter(BaseFormatter):
    def __init__(self, parsed_data, analyses):
        super().__init__(parsed_data, analyses)
        self.inner_url = parsed_data.get("vrai url", "")

    def format_report(self):
        data, comments = self.format_analyzers()
        return {
            "url_type": "nested",
            "parsed_url": self.parsed,
            "data": data,
            "comments": comments,
            "recommendation": self.get_recommendation(),
            "specific_insights": f"Nested URL: {self.inner_url[:50]}..." if self.inner_url else "Nested URL detected"
        }

class OpaqueFormatter(BaseFormatter):
    def __init__(self, parsed_data, analyses):
        super().__init__(parsed_data, analyses)
        self.scheme = parsed_data.get("schéma", "")

    def format_report(self):
        data, comments = self.format_analyzers()
        return {
            "url_type": "opac",
            "parsed_url": self.parsed,
            "data": data,
            "comments": comments,

            "recommendation": self.get_recommendation(),
            "specific_insights": f"Opaque URL with scheme '{self.scheme}'"
        }