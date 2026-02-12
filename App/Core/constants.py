URL_TYPES = {
    "HIERARCHICAL": "hierarchical",
    "OPAQUE": "opaque",
    "EMBEDDED": "embedded",
    "NESTED": "nested",
    "RELATIVE": "relative",
    "INVALID": "invalid"
}

HIERARCHICAL_SCHEMES = {
    "http", "https", "ftp", "ftps", "sftp", "ws", "wss", "file"
}

OPAQUE_SCHEMES = {
    "mailto", "tel", "sms", "urn", "geo", "magnet", "bitcoin"
}

EMBEDDED_SCHEMES = {
    "data", "blob"
}

NESTED_SCHEMES = {
    "view-source", "git+ssh", "jdbc", "jar"
}

URL_SEPARATORS = {
    "SCHEME": "://",
    "USERINFO": "@",
    "PORT": ":",
    "QUERY": "?",
    "FRAGMENT": "#",
    "PATH": "/"
}

CLASSIFIER_RULES = {
    "MAX_SCHEME_LENGTH": 15,
    "MAX_URL_LENGTH": 2048,
    "MIN_DOMAIN_LENGTH": 3
}

VALIDATION_STATUS = {
    "VALID": "valid",
    "INVALID": "invalid",
    "SUSPICIOUS": "suspicious"
}

NORMALIZATION_OPTIONS = {
    "LOWERCASE_SCHEME": True,
    "LOWERCASE_HOST": True,
    "STRIP_DEFAULT_PORT": True,
    "REMOVE_FRAGMENT": False
}