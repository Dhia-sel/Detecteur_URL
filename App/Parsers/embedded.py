from .base import BaseParser

class EmbeddedParser(BaseParser):
    def parse(self):
        parts=self.url.split(',',1)
        self.header=parts[0]
        self.info=parts[1]
        meta=self.header[5:].split(';')
        self.mime=meta[0] if meta[0] else "text/plain"
        self.is64="base64" in meta
    
    def data(self):
        self.parse()
        return {
            "schéma":"data",
            "type_média":self.mime,
            "longueur_données":len(self.info),
            "données":self.info[:20]+"...",
            "données_totales":self.info,
            "basée_64":self.is64,
        }
        