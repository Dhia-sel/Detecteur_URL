import math
class Lexical_Data_Analyzer:

    keys= [
        "login", "sign-in", "password", "credential", "unlock", "confirm", 
        "account", "verify", "session", "expired", "update", "recovery",

        "bank", "credit", "card", "billing", "invoice", "payment", "wallet",
        "paypal", "visa", "mastercard", "amex", "cvv", "security-code",
        
        "virus", "infected", "blocked", "suspended", "trojan", "call", 
        "support", "microsoft", "windows", "defender", "alert", "error",
        
        "google", "office365", "outlook", "adobe", "netflix", "amazon", 
        "dhl", "metamask", "coinbase", "binance", "trustwallet"]
   
    indicators= [
        "function", "var ", "const ", "let ", "document.", "window.", 
        "eval(", "exec(", "unescape", "atob(", "btoa(", "cookie", 
        "location.href", "xmlhttprequest", "fetch(", "post"]
    
    dangertags = [
        "<script", "<iframe", "<form", "<object", "<embed", "<input", "<html>"
    ]

    def __init__(self, parsed_data):
        self.content = parsed_data.get("données_décodés", "")
        if self.content is None:
            self.content = ""

    def _entropy(self, text):
        if not text: return 0
        prob = [float(text.count(c)) / len(text) for c in dict.fromkeys(list(text))]
        return -sum([p * math.log(p) / math.log(2.0) for p in prob])

    def analyze(self):
        text_lower = self.content.lower()
        semantic_score = 0
        for kw in self.keys:
            if kw in text_lower:
                semantic_score += 1
        code_score = 0
        for code_word in self.indicators:
            if code_word in text_lower:
                code_score += 1
        tag_count = 0
        for tag in self.dangertags:
            if tag in text_lower:
                tag_count += 1
        has_password_field = 1 if 'type="password"' in text_lower or "type='password'" in text_lower else 0
        entropy = self._entropy(self.content)
        code_chars = sum(text_lower.count(c) for c in ";{}<>()=\"")
        symbol_ratio = code_chars / len(text_lower) if len(text_lower) > 0 else 0

        return {
            "semantic_score": semantic_score, 
            "code_score": code_score,      
            "tag_count": tag_count,     
            "pwd_field": has_password_field, 
            "entropy": round(entropy, 4),
            "symbol_ratio": round(symbol_ratio, 2)
        }