from .base import BaseParser
from urllib.parse import parse_qs, urlparse

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
        ch=self.url.split(":", 1)
        self.inner=ch[1]
        self.wrapper={
            "schéma":ch[0],
            "hote": "aucun",
            "clef":"aucun"
        }

    def GetParam(self):
        clef="none"
        self.inner=None
        parsed = urlparse(self.url)
        params = parse_qs(parsed.query)
        for key in self.NESTED_KEYS:
            if key in params:
                clef=key
                self.inner=params[key][0]
                break
        if not self.inner and params:
            clef=list(params.keys())[0]
            self.inner=params[clef][0]
        self.wrapper={
            "schéma":parsed.scheme,
            "hote":parsed.netloc,
            "clef":clef
        }

    def parse(self):
        if self.IsPrefixBased():
            self.type="par préfixe"
            self.GetPrefix()
        else :
            self.type="par paramétre"
            self.GetParam()

    def data(self):
        self.parse()
        return {
           "type":self.type,
           "enveloppe":self.wrapper,
           "vrai url":self.inner

        }
    
        