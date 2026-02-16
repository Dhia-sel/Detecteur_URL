import math
class lexical_N_analyzer:
    keys= [
        "login", "signin", "log-in", "sign-in", "password", "credential", 
        "unlock", "verify", "verification", "secure", "security", "auth", 
        "account", "confirm", "recovery", "validate", "session", "update",
        
        "bank", "banking", "wallet", "payment", "invoice", "billing", 
        "paypal", "visa", "mastercard", "crypto", "bitcoin", "fund", 
        "transfer", "credit", "statement", "tax", "refund",
        
        "free", "gift", "bonus", "prize", "winner", "cash", "promo", 
        "urgent", "limited", "offer", "suspended", "blocked", "alert",
        
        "google", "apple", "icloud", "microsoft", "office", "outlook", 
        "netflix", "facebook", "linkedin", "amazon", "dhl", "fedex", 
        "ups", "dropbox", "adobe", "support", "service", "help"]

    sus_extentions= [".exe", ".zip", ".rar", ".7z", ".apk", ".scr", ".bat", ".php", ".html"]

    def __init__(self, parsed_data):
        self.wrapper = parsed_data.get("enveloppe", {})
        self.inner_url = parsed_data.get("vrai url", "")
        self.key = self.wrapper.get("clef", "")

    def entropy(self, text):
        if not text:return 0
        prob = [float(text.count(c)) / len(text) for c in dict.fromkeys(list(text))]
        return -sum([p * math.log(p) / math.log(2.0) for p in prob])

    def analyze(self):
        low= self.inner_url.lower()
        kw_count=0
        for kw in self.keys:
            if kw in low:
                kw_count += 1
        bad_ext=0
        for ext in self.sus_extentions:
            if ext in low:
                bad_ext=1
                break
        len_wrapper = len(self.wrapper.get("hote", ""))
        len_inner = len(self.inner_url)
        ratio = len_inner/len_wrapper if len_wrapper>0 else 0

        percent_count = self.inner_url.count('%') 
        equal_count = self.inner_url.count('=')   
        entropy = self.entropy(self.inner_url) 

        return {
            "keywords": kw_count,       
            "bad_extention":bad_ext, 
            "len_ratio": round(ratio, 2),
            "percent_count": percent_count,
            "equal_count": equal_count,
            "entropy": round(entropy, 4)
        }