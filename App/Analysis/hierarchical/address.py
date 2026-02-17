import ipaddress

class address_H_analyzer:
    SUSPICIOUS_TLDS = {'zip', 'xyz', 'top', 'gq', 'tk', 'ml', 'cf', 'work', 'loan'}

    def __init__(self, parsed_data):
        self.data = parsed_data
        self.host = parsed_data.get("auteur", {}).get("le hote", "")
        self.port = parsed_data.get("auteur", {}).get("port")
        self.scheme = parsed_data.get("schéma", "")

    def analyze(self):
        is_ip = False
        is_private = False
        try:
            ip = ipaddress.ip_address(self.host)
            is_ip = True
            is_private = ip.is_private
        except ValueError:
            pass

        std_ports = ['80', '443', None]
        abnormal_port = str(self.port) not in map(str, std_ports)

        is_sus_tld = False
        if not is_ip and '.' in self.host:
            tld = self.host.split('.')[-1].lower()
            is_sus_tld = tld in self.SUSPICIOUS_TLDS
        is_ssl = self.scheme.lower() in ['https', 'sftp']

        return {
            "is_ip": int(is_ip),
            "is_private": int(is_private),
            "abnormal_port": int(abnormal_port),
            "sus_tld": int(is_sus_tld),
            "is_ssl": int(is_ssl)
        }