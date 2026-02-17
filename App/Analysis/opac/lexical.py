import math
class lexical_O_analyzer:
    
    keys = [
        "urgent", "immediate", "now", "24h", "expire", "suspended", "blocked", 
        "action", "required", "critical", "alert", "warning", "final", "notice",
        
        "bitcoin", "btc", "eth", "wallet", "ledger", "trezor", "fund", "invest",
        "transfer", "wire", "bank", "invoice", "billing", "payment", "refund", 
        "tax", "irs", "fee", "cost", "owe", "debt", "paypal", "venmo", "cash",
        
        "login", "password", "verify", "secure", "account", "confirm", "code", 
        "pin", "otp", "credential", "update", "validate", "unlock",
        
        "winner", "prize", "gift", "free", "bonus", "lottery", "donation", 
        "charity", "claim", "reward", "won", "congrats", "offer",

        "delivery", "package", "track", "shipping", "dhl", "fedex", "ups", 
        "job", "hiring", "salary", "remote", "whatsapp", 
        "support", "service", "helpdesk", "admin", "hr", "payroll"
    ]

    def __init__(self, parsed_data):
        self.scheme = parsed_data.get("schéma", "").lower()
        self.destinations = parsed_data.get("destination", [])
        self.options = parsed_data.get("options", "")
        dests_str = " ".join(self.destinations) if self.destinations else ""
        self.full_text = (dests_str + " " + str(self.options)).lower()

    def _entropy(self, text):
        if not text: return 0
        prob = [float(text.count(c)) / len(text) for c in dict.fromkeys(list(text))]
        return -sum([p * math.log(p) / math.log(2.0) for p in prob])

    def analyze(self):
        kw_count = 0
        for key in self.keys:
            if key in self.full_text:
                kw_count += 1

        money_signs = self.full_text.count("$") + self.full_text.count("€") + self.full_text.count("£")
        dest_lens=0
        if self.destinations and len(self.destinations)>0:
            dest_lens= [len(k) for k in self.destinations]
        entropy = self._entropy(self.full_text)
        payload_len = len(self.options)

        return {
            "keywords": kw_count,  
            "money_signs": money_signs, 
            "dest_len": dest_lens,
            "payload_len": payload_len, 
            "entropy": round(entropy, 4)
        }