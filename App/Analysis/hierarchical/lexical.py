import math
import re
class lexical_H_analyzer:

    sus_keys = [
        "login", "signin", "log-in", "sign-in", "verify", "verification", 
        "account", "secure", "security", "update", "confirm", "auth", 
        "password", "recover", "unlock", "access", "validate",

        "bank", "banking", "transfer", "payment", "billing", "invoice", 
        "paypal", "visa", "mastercard", "amex", "wallet", "crypto", 
        "binance", "coinbase", "blockchain", "fund",

        "support", "service", "help", "client", "admin", "cs", 
        "dhl", "fedex", "usps", "delivery", "tracking",
        
        "free", "gift", "prize", "winner", "offer", "promo", 
        "urgent", "limited", "bonus", "cash"
    ]
    special= ['@','!','#','$','%','^','&','*','(',')','+','=','{','}','[',']','|','\\',';','"','\'','<','>',',','?','~','`','_']

    def __init__(self, parsed_data):
        self.host = parsed_data.get("auteur", {}).get("le hote", "")
        self.path = parsed_data.get("chemin", "")
        self.query = str(parsed_data.get("requete", ""))
        self.full_url = f"{self.host}{self.path}{self.query}"

    def entropy(self, text):
        if not text: return 0
        prob = [float(text.count(c))/len(text) for c in dict.fromkeys(list(text))]
        return -sum([p * math.log(p)/math.log(2.0) for p in prob])

    def analyze(self):
        url_len = len(self.full_url)
        num_special_chars = sum(self.full_url.count(char) for char in self.special)
        dot_count = self.full_url.count('.')
        dash_count = self.full_url.count('-')

        labels = self.host.rstrip('.').split('.') if self.host else []
        subdomain_depth = max(len(labels) - 2, 0)

        kw_count = 0
        tokens = set(re.findall(r"[a-z0-9]+", self.full_url.lower()))
        for kw in self.sus_keys:
            if kw in tokens:
                kw_count += 1

        entropy = self.entropy(self.host)
        digit_count = sum(c.isdigit() for c in self.full_url)
        digit_ratio = digit_count/url_len if url_len>0 else 0

        return {
            "len": url_len,
            "dots": dot_count,
            "dashes": dash_count,
            "special_chars": num_special_chars,
            "subdomain_depth": subdomain_depth,   
            "keywords": kw_count,
            "entropy": round(entropy, 4),
            "digitRatio": round(digit_ratio, 3)
        }
  