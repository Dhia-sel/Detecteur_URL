from .classifier import URLClassifier
from .normalizer import URLNormalizer
from ..Parsers.hierarchical import HierarchicalParser
from ..Parsers.embedded import EmbeddedParser
from ..Parsers.nested import NestedParser
from ..Parsers.opaque import OpacParser
from ..Analysis.hierarchical.lexical import lexical_H_analyzer
from ..Analysis.hierarchical.behaviour import behaviour_H_analyzer
from ..Analysis.hierarchical.address import address_H_analyzer
from ..Analysis.embedded.lexical import lexical_E_analyzer
from ..Analysis.embedded.behaviour import behaviour_E_analyzer
from ..Analysis.nested.lexical import lexical_N_analyzer
from ..Analysis.nested.behaviour import behaviour_N_analyzer
from ..Analysis.opac.lexical import lexical_O_analyzer
from ..Analysis.opac.behaviour import behaviour_O_analyzer
from ..Explaining.formatter import HierarchicalFormatter, EmbeddedFormatter, NestedFormatter, OpaqueFormatter


class URLAnalyzerPipeline:
    
    def __init__(self, url):
        self.original_url = url
        self.normalized_url = None
        self.url_type = None
        self.parsed_data = None
        self.analyses = {}
        self.formatted_report = None
    
    def normalize(self):
        normalizer = URLNormalizer(self.original_url)
        self.normalized_url = normalizer.normalize_url()
        return self.normalized_url
    
    def classify(self):
        classifier = URLClassifier(self.normalized_url)
        classification = classifier.classify()
        type_map = {
            "embarqué": "embedded",
            "imbriqué": "nested",
            "hiérarchique": "hierarchical",
            "opaque": "opaque",
            "url invalide": "invalid"
        }
        self.url_type = type_map.get(classification, "invalid")
        return self.url_type
    
    def parse(self):
        if self.url_type == "hierarchical":
            parser = HierarchicalParser(self.normalized_url)
        elif self.url_type == "embedded":
            parser = EmbeddedParser(self.normalized_url)
        elif self.url_type == "nested":
            parser = NestedParser(self.normalized_url)
        elif self.url_type == "opaque":
            parser = OpacParser(self.normalized_url)
        else:
            raise ValueError(f"Type d'URL invalide: {self.url_type}")
        
        self.parsed_data = parser.data()
        return self.parsed_data
    
    def analyze_hierarchical(self):

        address_analyzer = address_H_analyzer(self.parsed_data)
        lexical_analyzer = lexical_H_analyzer(self.parsed_data)
        behaviour_analyzer = behaviour_H_analyzer(self.parsed_data)
        
        self.analyses = {
            "address": address_analyzer.analyze(),
            "lexical": lexical_analyzer.analyze(),
            "behaviour": behaviour_analyzer.analyze()
        }
    
    def analyze_embedded(self):

        lexical_analyzer = lexical_E_analyzer(self.parsed_data)
        behaviour_analyzer = behaviour_E_analyzer(self.parsed_data)
        
        self.analyses = {
            "lexical": lexical_analyzer.analyze(),
            "behaviour": behaviour_analyzer.analyze()
        }
    
    def analyze_nested(self):

        lexical_analyzer = lexical_N_analyzer(self.parsed_data)
        behaviour_analyzer = behaviour_N_analyzer(self.parsed_data)
        
        self.analyses = {
            "lexical": lexical_analyzer.analyze(),
            "behaviour": behaviour_analyzer.analyze()
        }
    
    def analyze_opaque(self):
        lexical_analyzer = lexical_O_analyzer(self.parsed_data)
        behaviour_analyzer = behaviour_O_analyzer(self.parsed_data)
        
        self.analyses = {
            "lexical": lexical_analyzer.analyze(),
            "behaviour": behaviour_analyzer.analyze()
        }
    
    def analyze(self):

        if self.url_type == "hierarchical":
            self.analyze_hierarchical()
        elif self.url_type == "embedded":
            self.analyze_embedded()
        elif self.url_type == "nested":
            self.analyze_nested()
        elif self.url_type == "opaque":
            self.analyze_opaque()
        else:
            raise ValueError(f"Type d'URL invalide pour l'analyse: {self.url_type}")
        
        return self.analyses
    
    def format_report(self):
        if self.url_type == "hierarchical":
            formatter = HierarchicalFormatter(self.parsed_data, self.analyses)
        elif self.url_type == "embedded":
            formatter = EmbeddedFormatter(self.parsed_data, self.analyses)
        elif self.url_type == "nested":
            formatter = NestedFormatter(self.parsed_data, self.analyses)
        elif self.url_type == "opaque":
            formatter = OpaqueFormatter(self.parsed_data, self.analyses)
        else:
            raise ValueError(f"Type d'URL invalide pour la formatage: {self.url_type}")
        
        self.formatted_report = formatter.format_report()
        return self.formatted_report
    
    def run(self):
        try:
            self.normalize()
            self.classify()
            self.parse()
            self.analyze()
            self.format_report()
            return {
                "success": True,
                "url_type": self.url_type,
                "report": self.formatted_report
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
