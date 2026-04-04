from .messages import RISK_MESSAGES, FEATURE_MESSAGES


FEATURE_RISK = {
    "is_ip": "high_bad",
    "is_private": "high_bad",
    "abnormal_port": "high_bad",
    "sus_tld": "high_bad",
    "is_ssl": "high_good",
    "entropy": "high_bad",
    "special_chars": "high_bad",
    "sus_keywords": "high_bad",
    "url_len": "high_bad",
    "dot_count": "high_bad",
    "dash_count": "high_bad",
    "subdomain_depth": "high_bad",
    "has_redirection": "high_bad",
    "has_obfuscation": "high_bad",
    "is_shortened": "high_bad",
    "multi_subdomain": "high_bad",
    "double_slash": "high_bad",
    "kw_count": "high_bad",
    "bad_ext": "high_bad",
    "ratio": "high_bad",
    "percent_count": "high_bad",
    "equal_count": "high_bad",
    "keywords": "high_bad",
    "money_signs": "high_bad",
    "dest_lens": "high_bad",
    "payload_len": "high_bad",
    "trusted_wrapper": "high_good",
    "downgrade": "high_bad",
    "is_external": "high_bad",
    "key_standard": "high_good",
    "target_digit": "high_bad",
    "is_risky": "high_bad",
    "dest_count": "high_bad",
    "multi_target": "high_bad",
    "has_options": "high_bad",
    "risky_payload": "high_bad"
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
            if sub_key in FEATURE_MESSAGES:
                risk_type = FEATURE_RISK.get(sub_key, "high_bad")
                if (risk_type == "high_bad" and sub_value > 0) or (risk_type == "high_good" and sub_value == 0):
                    comments.append(FEATURE_MESSAGES[sub_key]['hazardous'])
                elif (risk_type == "high_bad" and sub_value == 0) or (risk_type == "high_good" and sub_value > 0):
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
        hazardous_count = 0
        for analyzer, values in self.analyses.items():
            for sub_key, sub_value in values.items():
                risk_type = FEATURE_RISK.get(sub_key, "high_bad")
                if (risk_type == "high_bad" and sub_value > 0) or (risk_type == "high_good" and sub_value == 0):
                    hazardous_count += 1
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
        self.data_type = parsed_data.get("type", "")

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
        self.nested_urls = parsed_data.get("urls_imbriquées", [])

    def format_report(self):
        data, comments = self.format_analyzers()
        return {
            "url_type": "nested",
            "parsed_url": self.parsed,
            "data": data,
            "comments": comments,
            "recommendation": self.get_recommendation(),
            "specific_insights": f"Contains {len(self.nested_urls)} nested URLs"
        }

class OpaqueFormatter(BaseFormatter):
    def __init__(self, parsed_data, analyses):
        super().__init__(parsed_data, analyses)
        self.scheme = parsed_data.get("schéma", "")

    def format_report(self):
        data, comments = self.format_analyzers()
        return {
            "url_type": "opaque",
            "parsed_url": self.parsed,
            "data": data,
            "comments": comments,

            "recommendation": self.get_recommendation(),
            "specific_insights": f"Opaque URL with scheme '{self.scheme}'"
        }