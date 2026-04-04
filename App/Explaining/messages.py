RISK_MESSAGES = {
    "low": "This URL appears safe based on our analysis. No major red flags detected.",
    "medium": "Caution advised. Some suspicious elements were found, but not conclusive evidence of phishing.",
    "high": "High risk detected! This URL shows strong indicators of being malicious. Do not proceed."
}

FEATURE_MESSAGES = {
    "is_ip": {
        "hazardous": "The host is an IP address, which can be suspicious if unexpected.",
        "safe": "The host is a domain name, not an IP address."
    },
    "is_private": {
        "hazardous": "The IP address is private (local network), which may indicate internal access.",
        "safe": "The IP address is public."
    },
    "abnormal_port": {
        "hazardous": "Uses a non-standard port (not 80 or 443).",
        "safe": "Uses standard ports (80 for HTTP or 443 for HTTPS)."
    },
    "sus_tld": {
        "hazardous": "Uses a suspicious top-level domain.",
        "safe": "Uses a standard top-level domain."
    },
    "is_ssl": {
        "hazardous": "Does not use HTTPS (not secure).",
        "safe": "Uses HTTPS for secure communication."
    },
    "entropy": {
        "hazardous": "High character randomness detected, possibly indicating obfuscation.",
        "safe": "Normal character distribution."
    },
    "special_chars": {
        "hazardous": "Contains many special characters, which may be used for evasion.",
        "safe": "Contains few special characters."
    },
    "sus_keywords": {
        "hazardous": "Contains suspicious keywords (e.g., login, verify, account).",
        "safe": "No suspicious keywords detected."
    },
    "has_redirection": {
        "hazardous": "Contains redirection parameters in the query.",
        "safe": "No redirection parameters found."
    },
    "has_obfuscation": {
        "hazardous": "Signs of obfuscation detected (e.g., embedded credentials).",
        "safe": "No obfuscation detected."
    },
    "is_shortened": {
        "hazardous": "Uses a URL shortener service.",
        "safe": "Does not use a URL shortener."
    },
    "multi_subdomain": {
        "hazardous": "Has excessive subdomains.",
        "safe": "Has a normal number of subdomains."
    },
    "double_slash": {
        "hazardous": "Contains double slashes in the path, potentially a bypass attempt.",
        "safe": "No double slashes in the path."
    }
}

GENERAL_TIPS = [
    "Always verify URLs before clicking.",
    "Check for HTTPS and valid certificates.",
    "Be wary of unsolicited links.",
    "Use antivirus software with URL scanning."
]