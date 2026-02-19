import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
parent_dir1 = os.path.dirname(parent_dir)
src_path = os.path.join(parent_dir1, 'Projet-Detecteur-Url')
sys.path.append(src_path)

from App.Parsers.nested import NestedParser
from App.Analysis.nested.lexical import lexical_N_analyzer
from App.Analysis.nested.behaviour import behaviour_N_analyzer
from App.Core.normalizer import URLNormalizer

test_url = [
    "https://www.facebook.com/l.php?u=http://phishing-bank.com/login.php",
    "http://newsletter.company.com/track?dest=https://104.28.19.50/malware.exe",
    "view-source:https://obfuscated-site.com/index.html?redirect=http://evil.com",
    "https://proxy-anonymizer.net/go/http://malicious-domain.onion/hidden",
    "https://sso.corporate.com/auth?next=ws://192.168.1.10:5000/stream",
    "filesystem:http://localhost/temporary/ftp://attacker.com/stealer.zip",
    "https://web.archive.org/web/20230101/http://old-phish.com/login",
    "http://click-tracker.net/out?link=https://app.bad-site.com/download.apk",
    "https://www.google.com/url?q=http://172.16.254.1/router-exploit.sh",
    "https://secure-gateway.com/bypass//http://c2-server.com/beacon"
]
for url in test_url:
    Normal=URLNormalizer(url)
    Nurl=Normal.normalize_url()
    n=NestedParser(Nurl)
    parsed=n.data()
    a1=lexical_N_analyzer(parsed)
    a2=behaviour_N_analyzer(parsed)
    print(f"data parsee: \n {parsed}")
    print(f"analyse lexique \n {a1.analyze()}")
    print(f"analyse de comportement \n {a2.analyze()}")
    print("")
    print("")

