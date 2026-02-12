from base import BaseParser
from urllib.parse import unquote
import base64

class EmbeddedParser(BaseParser):
    def __init__(self, url):
        super().__init__(url)
        self.mime = ""
        self.is64 =False
        self.info =""
        self.decoded=""

    def parse(self):
        if ',' in self.url:
            header, self.info = self.url.split(',', 1)
        else:
            header = self.url
            self.info = ""
        if len(header) > 5: 
            meta = header[5:].split(';')
            self.mime = meta[0] if meta[0] else "text/plain"
            self.is64 = "base64" in [m.lower() for m in meta]
        else:
            self.mime = "inconnu"
            self.is64 = False
        if self.info:
            if self.is64:
                try:
                    self.decoded = base64.b64decode(self.info).decode('utf-8', errors='replace')
                except Exception:
                    self.decoded = "[Erreur de décodage]"
            else:
                self.decoded = unquote(self.info)
        else:
            self.decoded = ""
    
    def data(self):
        self.parse()
        return {
            "schéma":"data",
            "type_média":self.mime,
            "longueur_données":len(self.info),
            "données":self.info[:20]+"...",
            "données_totales":self.info,
            "données_décodés":self.decoded,
            "basée_64":self.is64,
        }
        