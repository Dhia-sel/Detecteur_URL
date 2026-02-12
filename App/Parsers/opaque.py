from base import BaseParser
from urllib import urlparse

class OpacParser(BaseParser):
    def parse(self):
        p=urlparse(self.url)
        return p
    
    def data(self):
        p=self.parse()
        return {
            "schéma":p.scheme,
            "destination":p.path,
            "options":p.query
        }