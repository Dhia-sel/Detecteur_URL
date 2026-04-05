RISK_MESSAGES = {
    "low": "This URL appears safe based on our analysis. No major red flags detected.",
    "medium": "Caution advised. Some suspicious elements were found, but not conclusive evidence of phishing.",
    "high": "High risk detected! This URL shows strong indicators of being malicious. Do not proceed."
}

FEATURE_MESSAGES = {
    # Address Analyzer
    "is_ip": {
        "hazardous": "The host is an IP address instead of a domain name, which is suspicious.",
        "safe": "Uses a domain name instead of an IP address."
    },
    "is_private": {
        "hazardous": "Uses a private IP address, indicating potential internal network access.",
        "safe": "Uses a public IP address."
    },
    "abnormal_port": {
        "hazardous": "Uses a non-standard port (not 80 for HTTP or 443 for HTTPS).",
        "safe": "Uses standard web ports (80 or 443)."
    },
    "sus_tld": {
        "hazardous": "Uses a suspicious top-level domain known for phishing.",
        "safe": "Uses a legitimate top-level domain."
    },
    "is_ssl": {
        "hazardous": "Does not use HTTPS/SSL encryption; connection is insecure.",
        "safe": "Uses HTTPS/SSL for secure encrypted communication."
    },
    # Lexical Analyzer - Hierarchical
    "len": {
        "hazardous": "URL is unusually long, often used to hide malicious intent.",
        "safe": "URL has a reasonable length."
    },
    "dots": {
        "hazardous": "Contains excessive dots, which can confuse the URL parsing.",
        "safe": "Contains a normal number of dots."
    },
    "dashes": {
        "hazardous": "Contains many dashes, potentially used for obfuscation.",
        "safe": "Contains few or no dashes."
    },
    "special_chars": {
        "hazardous": "Contains numerous special characters, likely used for evasion.",
        "safe": "Contains few special characters."
    },
    "subdomain_depth": {
        "hazardous": "Has excessive subdomain levels, typical of phishing sites.",
        "safe": "Has normal subdomain depth."
    },
    "keywords": {
        "hazardous": "Contains suspicious keywords associated with phishing (login, verify, etc.).",
        "safe": "No suspicious keywords detected."
    },
    "entropy": {
        "hazardous": "High character randomness indicates potential obfuscation or encoding.",
        "safe": "Normal character distribution."
    },
    "digitRatio": {
        "hazardous": "Contains high proportion of digits, often seen in malicious URLs.",
        "safe": "Contains normal proportion of digits."
    },
    # Behaviour Analyzer - Hierarchical
    "has_redirection": {
        "hazardous": "Contains URL redirection parameters in the query string.",
        "safe": "No redirection parameters detected."
    },
    "has_obfuscation": {
        "hazardous": "Contains embedded credentials or other obfuscation techniques.",
        "safe": "No embedded credentials detected."
    },
    "is_shortened": {
        "hazardous": "Uses a URL shortener service, hiding the true destination.",
        "safe": "Does not use a URL shortener."
    },
    "multi_subdomain": {
        "hazardous": "Has multiple subdomain levels, often used in phishing.",
        "safe": "Has a normal number of subdomains."
    },
    "double_slash": {
        "hazardous": "Contains double slashes in the path, a potential bypass technique.",
        "safe": "No suspicious double slashes detected."
    },
    # Lexical Analyzer - Embedded
    "semantic_score": {
        "hazardous": "Contains several suspicious semantic terms (login, verify, etc.).",
        "safe": "Contains no suspicious terms."
    },
    "code_score": {
        "hazardous": "Contains signs of malicious code indicators.",
        "safe": "No harmful code indicators detected."
    },
    "tag_count": {
        "hazardous": "Contains dangerous HTML/script tags like <script>, <iframe>, <form>.",
        "safe": "No dangerous tags detected."
    },
    "pwd_field": {
        "hazardous": "Contains password input fields, likely for credential theft.",
        "safe": "No password fields detected."
    },
    "symbol_ratio": {
        "hazardous": "Has high ratio of code symbols, indicating obfuscated code.",
        "safe": "Has normal symbol distribution."
    },
    # Behaviour Analyzer - Embedded
    "risky_mime": {
        "hazardous": "Uses a risky MIME type (JavaScript, HTML, executable, etc.).",
        "safe": "Uses a safe MIME type."
    },
    "base64": {
        "hazardous": "Content is base64 encoded, common in phishing attacks.",
        "safe": "Content is not encoded."
    },
    "hidden_html": {
        "hazardous": "Contains HTML content hidden with base64 encoding.",
        "safe": "No hidden HTML detected."
    },
    "is_unknown": {
        "hazardous": "Uses an unknown or suspicious MIME type.",
        "safe": "Uses a recognized MIME type."
    },
    "small_payload": {
        "hazardous": "Small payload size typical of simple phishing pages.",
        "safe": "Payload size is normal or large."
    },
    # Lexical Analyzer - Nested
    "bad_extention": {
        "hazardous": "Contains suspicious file extensions (.exe, .zip, .apk, etc.).",
        "safe": "No suspicious file extensions detected."
    },
    "len_ratio": {
        "hazardous": "Nested URL is disproportionately longer than the wrapper.",
        "safe": "URL lengths are proportional."
    },
    "percent_count": {
        "hazardous": "Contains percent-encoded characters, potentially hiding content.",
        "safe": "No suspicious percent encoding detected."
    },
    "equal_count": {
        "hazardous": "Contains multiple equals signs, suspicious in nested URLs.",
        "safe": "Normal number of equals signs."
    },
    # Behaviour Analyzer - Nested
    "trusted_wrapper": {
        "hazardous": "Wrapper domain is not from a trusted company.",
        "safe": "Wrapper domain is from a trusted company (Google, Facebook, etc.)."
    },
    "downgrade": {
        "hazardous": "HTTPS is downgraded to HTTP in the nested URL.",
        "safe": "No security downgrade detected."
    },
    "is_external": {
        "hazardous": "Nested URL points to an external domain, not the wrapper.",
        "safe": "Nested URL points to the same domain."
    },
    "key_standard": {
        "hazardous": "Uses non-standard parameter names for the nested URL.",
        "safe": "Uses standard parameter names."
    },
    "target_digit": {
        "hazardous": "Nested URL starts with a digit, suspicious behavior.",
        "safe": "Nested URL starts with a normal character."
    },
    # Lexical Analyzer - Opaque
    "money_signs": {
        "hazardous": "Contains currency symbols ($, €, £), typical of financial phishing.",
        "safe": "No currency symbols detected."
    },
    "dest_len": {
        "hazardous": "Has unusual destination structure with suspicious length patterns.",
        "safe": "Destination structure is normal."
    },
    "payload_len": {
        "hazardous": "Payload is large, possibly containing malicious data.",
        "safe": "Payload size is reasonable."
    },
    # Behaviour Analyzer - Opaque
    "is_risky": {
        "hazardous": "Uses a risky scheme (bitcoin, mailto, javascript, etc.).",
        "safe": "Uses a standard scheme."
    },
    "dest_count": {
        "hazardous": "Has multiple destinations, unusual for legitimate URLs.",
        "safe": "Has a single destination."
    },
    "multi_target": {
        "hazardous": "Targets multiple recipients within parameters.",
        "safe": "Targets a single recipient."
    },
    "has_options": {
        "hazardous": "Contains options/parameters, often used for phishing attacks.",
        "safe": "No suspicious parameters found."
    },
    "risky_payload": {
        "hazardous": "Combines risky scheme with options/payload, highly suspicious.",
        "safe": "No risky payload combination detected."
    }
}

GENERAL_TIPS = [
    "Always verify URLs before clicking.",
    "Check for HTTPS and valid certificates.",
    "Be wary of unsolicited links.",
    "Use antivirus software with URL scanning."
]