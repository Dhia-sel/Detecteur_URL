from base import BaseParser
from urllib import urlparse

class HierarchicalParser(BaseParser):
    def parse(self):
        p=urlparse(self.url)
        return p
    
    def data(self):
        p=self.parse()
        return {
            "schéma": p.scheme,
            "auteur":{
                "utilisateur":p.username,
                "mot de passe":p.password,
                "le hote":p.hostname,
                "port":p.port,
            },
            "chemin":p.path,
            "requete":p.query,
            "fragment":p.fragment
        }
    