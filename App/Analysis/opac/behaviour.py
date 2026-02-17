class Behaviour_Opaque_Analyzer:

    risky = [
        "mailto", "tel", "sms", "mms", "fax", "news", "nntp",     
        "bitcoin", "ethereum", "cashapp", "venmo", "pay",           
        "javascript", "vbscript", "data", "blob", "files", "about"  ]

    def __init__(self, parsed_data):
        self.scheme = parsed_data.get("schéma", "").lower()
        self.destinations = parsed_data.get("destination", [])
        self.options = parsed_data.get("options", "")

    def analyze(self):
        risky_scheme = 0
        if self.scheme in self.risky:
            risky_scheme = 1
        dest_count = len(self.destinations)
        multi_target = 1 if dest_count > 1 else 0
        has_options = 1 if len(self.options) > 0 else 0
        with_payload = 1 if (risky_scheme and has_options) else 0

        return {
            "is_risky": risky_scheme,    
            "dest_count": dest_count,         
            "multi_target": multi_target,  
            "has_options": has_options,       
            "risky_payload": with_payload 
        }