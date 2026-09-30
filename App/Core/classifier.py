import re
from urllib.parse import parse_qsl, urlparse

class URLClassifier():
    NESTED_QUERY_KEYS = {
        "url", "u", "link", "target", "dest", "destination", "next",
        "redirect", "redirect_url", "continue", "return", "q",
    }

    def __init__(self, url):
        self.url=url
        self.parsed=urlparse(self.url)

    def isAbsolute(self):
        return '://' in self.url
    
    def countBeforeSlash(self):
        if "://" in self.url:
            prefix = self.url.split("://")[0]
            return prefix.count(":")
        return 0
    
    def hasURL(self):
        for key, value in parse_qsl(self.parsed.query, keep_blank_values=True):
            if key.lower() in self.NESTED_QUERY_KEYS and re.search(
                r"[a-z][a-z0-9+.-]*:", value, re.IGNORECASE
            ):
                return True
        return False
    
    def embedded(self):
        return self.url.lower().startswith("data:")

    def hierarchical(self):
        return self.isAbsolute() and self.countBeforeSlash()==0

    def nested(self):
        c1=self.isAbsolute() and self.countBeforeSlash()>=1
        return c1 or self.hasURL()
    def opac(self):
        c1=self.parsed.scheme and not self.isAbsolute()
        return c1 and not self.embedded()
    
    def classify(self):
        if self.embedded():
            return "embarqué"
        elif self.nested():
            return "imbriqué"
        elif self.hierarchical():
            return "hiérarchique"
        elif self.opac():
            return "opaque"
        else:
            return "url invalide"      
        

