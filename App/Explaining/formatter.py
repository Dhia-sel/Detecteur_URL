from .messages import RISK_MESSAGES, FEATURE_MESSAGES

class BaseFormatter:
    def __init__(self, parsed_data, analyses):
        self.parsed = parsed_data
        self.analyses = analyses

    def format_hazardous_stats(self):
        """Retourner des messages lisibles par l'homme pour les caractéristiques dangereuses."""
        messages = []
        for key, value in self.analyses.items():
            if isinstance(value, dict):
                for sub_key, sub_value in value.items():
                    if sub_value > 0 and sub_key in FEATURE_MESSAGES:
                        messages.append(f"{sub_key}: {sub_value} - {FEATURE_MESSAGES[sub_key]['hazardous']}")
        return messages

    def format_safe_stats(self):
        """Retourner des messages lisibles par l'homme pour les caractéristiques sûres."""
        messages = []
        for key, value in self.analyses.items():
            if isinstance(value, dict):
                for sub_key, sub_value in value.items():
                    if sub_value == 0 and sub_key in FEATURE_MESSAGES:
                        messages.append(f"{sub_key}: {sub_value} - {FEATURE_MESSAGES[sub_key]['safe']}")
        return messages

    def get_recommendation(self):
        hazardous_count = len(self.format_hazardous_stats())
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
        return {
            "url_type": "hierarchical",
            "parsed_url": self.parsed,
            "hazardous_stats": self.format_hazardous_stats(),
            "safe_stats": self.format_safe_stats(),
            "recommendation": self.get_recommendation(),
            "specific_insights": f"Host: {self.host}, Scheme: {self.scheme}"
        }

class EmbeddedFormatter(BaseFormatter):
    def __init__(self, parsed_data, analyses):
        super().__init__(parsed_data, analyses)
        self.data_type = parsed_data.get("type", "")

    def format_report(self):
        return {
            "url_type": "embedded",
            "parsed_url": self.parsed,
            "hazardous_stats": self.format_hazardous_stats(),
            "safe_stats": self.format_safe_stats(),
            "recommendation": self.get_recommendation(),
            "specific_insights": f"Embedded data type: {self.data_type}"
        }

class NestedFormatter(BaseFormatter):
    def __init__(self, parsed_data, analyses):
        super().__init__(parsed_data, analyses)
        self.nested_urls = parsed_data.get("urls_imbriquées", [])

    def format_report(self):
        return {
            "url_type": "nested",
            "parsed_url": self.parsed,
            "hazardous_stats": self.format_hazardous_stats(),
            "safe_stats": self.format_safe_stats(),
            "recommendation": self.get_recommendation(),
            "specific_insights": f"Contains {len(self.nested_urls)} nested URLs"
        }

class OpaqueFormatter(BaseFormatter):
    def __init__(self, parsed_data, analyses):
        super().__init__(parsed_data, analyses)
        self.scheme = parsed_data.get("schéma", "")

    def format_report(self):
        return {
            "url_type": "opaque",
            "parsed_url": self.parsed,
            "hazardous_stats": self.format_hazardous_stats(),
            "safe_stats": self.format_safe_stats(),
            "recommendation": self.get_recommendation(),
            "specific_insights": f"Opaque scheme: {self.scheme}"
        }