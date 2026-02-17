class behaviour_E_analyzer:
    risky= {
    "text/html",
    "text/javascript",
    "application/javascript",
    "application/x-javascript",
    "application/ecmascript",
    "text/ecmascript",
    "text/jscript",
    "text/vbscript",
    "application/vbscript",
    "text/livescript",
    "application/x-msdownload",
    "application/x-dosexec",
    "application/octet-stream",
    "application/java-archive",
    "application/x-shockwave-flash",
    "application/hta",
    "text/x-scriptlet",
    "text/x-component",
    "image/svg+xml",
    "application/x-sh",
    "application/x-csh",
    "text/x-php",
    "application/x-powershell",
    "application/pdf",
    "application/msword",
    "application/vnd.ms-excel",
    "application/rtf",
    "application/vnd.ms-excel.sheet.macroenabled.12",
    "application/vnd.ms-word.document.macroenabled.12"}

    def __init__(self, parsed_data):
        self.mime = parsed_data.get("type_média", "").lower()
        self.is_base64 = parsed_data.get("basée_64", False)
        self.total_data_len = len(parsed_data.get("données_totales", ""))

    def analyze(self):
        risky_mime = 0
        for risk in self.risky:
            if self.mime.startswith(risk):
                risky_mime = 1
                break
        unknown_mime = 1 if not self.mime else 0
        is_b64 = 1 if self.is_base64 else 0
        hidden_html = 1 if risky_mime and is_b64 else 0
        small_payload = 1 if self.total_data_len < 5000 else 0
        return {
            "risky_mime": risky_mime, 
            "base64": is_b64,         
            "hidden_html": hidden_html, 
            "is_unknown": unknown_mime,
            "small_payload":small_payload 
        }