from base import BaseParser
from urllib.parse import urlparse,parse_qs

class OpacParser(BaseParser):
    def parse(self):
        p=urlparse(self.url)
        self.scheme=p.scheme
        if p.query:
            self.options = parse_qs(p.query, keep_blank_values=True)
        else:
            self.options = {}
        raw_dest=p.path.replace(';',',')
        if raw_dest:
            self.destination = [x.strip() for x in raw_dest.split(',') if x.strip()]
        else:
            self.destination =[]

    def data(self):
        self.parse()
        return {
            "schéma":self.scheme,
            "destination":self.destination,
            "options":self.options
        }