from .base import BaseParser
from urllib.parse import parse_qs, urlparse

class NestedParser(BaseParser):
    keys = {'url',
                'redirect',
                'redirect_url',
                'next',
                'target',
                'dest',
                'u',
                'link',
                'src'}
    
    def __init__(self, url):
        super().__init__(url)
        self.type = ""  
        self.inner = ""       
        self.wrapper = {        
            "schéma": "",
            "hote": "",
            "clef": ""}
    
    def IsPrefixBased(self):
        if ":" not in self.url:
            return False
        scheme =self.url.split(":", 1)[0]
        if self.url.startswith(scheme + "://"):
            return False
        return True
    
    def GetPrefix(self):
        ch=self.url.split(":", 1)
        inner_url=ch[1]
        if inner_url.startswith('http:/') and not inner_url.startswith('http://'):
            inner_url = inner_url.replace('http:/', 'http://', 1)
        elif inner_url.startswith('https:/') and not inner_url.startswith('https://'):
            inner_url = inner_url.replace('https:/', 'https://', 1)
        self.inner=inner_url
        self.wrapper={
            "schéma":ch[0],
            "hote": "aucun",
            "clef":"aucun"
        }

    def GetParam(self):
        parsed = urlparse(self.url)
        params = parse_qs(parsed.query)
        found_key = "aucun"
        extracted_url = ""
        found_keys = self.keys.intersection(params.keys())
        if found_keys:
            found_key = list(found_keys)[0]
            extracted_url = params[found_key][0]
        elif params:
            for k, v in params.items():
                val = v[0]
                if val.startswith(('http:', 'https:', 'www.','ws:','wss:','ftp:')):
                    found_key = k
                    extracted_url = val
                    break
        self.inner = extracted_url
        self.wrapper = {
            "schéma": parsed.scheme,
            "hote": parsed.netloc,
            "clef": found_key
        }

    def parse(self):
        if self.IsPrefixBased():
            self.type="par préfixe"
            self.GetPrefix()
        elif '?' in self.url:
            self.GetParam()
            if self.inner:
                self.type="par paramétre"
            else:
                self.type="Aucun"
        else:
            self.type="Aucun"
        if self.type == "Aucun" or not self.inner:
            for indicateur in ['http://', 'https://', 'http:/', 'https:/']:
                pos = self.url.find(indicateur, 8) 
                if pos != -1:
                    inner_url = self.url[pos:]
                    if inner_url.startswith('http:/') and not inner_url.startswith('http://'):
                        inner_url = inner_url.replace('http:/', 'http://', 1)
                    elif inner_url.startswith('https:/') and not inner_url.startswith('https://'):
                        inner_url = inner_url.replace('https:/', 'https://', 1)
                        
                    self.inner = inner_url
                    self.type = "dans le chemin"
                    self.wrapper["clef"] = "chemin"
                    break

    def data(self):
        self.parse()
        return {
           "type":self.type,
           "enveloppe":self.wrapper,
           "vrai url":self.inner }
    
        