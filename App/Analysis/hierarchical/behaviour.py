class behaviour_H_analyzer:
    SHORTENERS = {'bit.ly', 'goo.gl', 'tinyurl.com', 't.co', 'ow.ly', 'is.gd', 'buff.ly'}

    def __init__(self, parsed_data):
        self.data = parsed_data
        self.user = parsed_data.get("auteur", {}).get("utilisateur")
        self.password = parsed_data.get("auteur", {}).get("mot de passe")
        self.host = parsed_data.get("auteur", {}).get("le hote", "")
        self.query = str(parsed_data.get("requete", ""))
        self.path = parsed_data.get("chemin", "")

    def analyze(self):
        has_redirection = 0
        if "http" in self.query or "www" in self.query:
            has_redirection=1

        has_obfuscation = 0
        if self.user not in [None,"aucun"] or self.password not in [None, "aucun"]:
            has_obfuscation = 1
            
        is_shortened = 0
        if self.host.lower() in self.SHORTENERS:
            is_shortened = 1

        subdomain_count = self.host.count('.')
        is_multi_subdomain = 1 if subdomain_count > 3 else 0
        has_double_slash = 1 if "//" in self.path else 0

        return {
            "has_redirection": has_redirection,
            "has_obfuscation": has_obfuscation,
            "is_shortened": is_shortened,
            "multi_subdomain": is_multi_subdomain,
            "double_slash": has_double_slash
        }