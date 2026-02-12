from urllib.parse import urlparse

class URLClassifier():
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
        return "url=" in self.parsed.query
    
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
        

