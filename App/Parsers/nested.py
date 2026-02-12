from .base import BaseParser
from urllib import parse_qs, urlparse

class NestedParser(BaseParser):
    NESTED_KEYS = {'url',
                'redirect',
                'redirect_url',
                'next',
                'target',
                'dest',
                'u',
                'link',
                'src'}
    
    def IsPrefixBased(self):
        if ":" not in self.url:
            return False
        scheme =self.url.split(":", 1)[0]
        if self.url.startswith(scheme + "://"):
            return False
        return True
    
    def IsParamBased(self):
        parsed = urlparse(self.url)
        if not parsed.query:
            return False
        keys = parse_qs(parsed.query).keys()
        return bool(self.NESTED_KEYS.intersection(keys))
    
    def GetPrefix(self):
        return url.split(":", 1)[1]
    
    def GetParam(self):
        parsed = urlparse(self.url)
        params = parse_qs(parsed.query)
        for key in self.NESTED_KEYS:
            if key in params:
                return params[key][0]
        return None

    def parse(self):
        if self.IsPrefixBased():
            self.type="par préfixe"
            self.inner=self.GetPrefix()
        elif self.IsParamBased():
            self.type="par paramétre"
            self.inner=self.GetParam()

    def data(self):
        self.parse()
        return {
           "type":self.type,
           "vrai url":self.inner

        }
    
        