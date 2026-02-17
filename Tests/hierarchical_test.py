import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
parent_dir1 = os.path.dirname(parent_dir)
src_path = os.path.join(parent_dir1, 'Projet-Detecteur-Url')
sys.path.append(src_path)

from App.Parsers.hierarchical import HierarchicalParser
from App.Analysis.hierarchical.lexical import lexical_H_analyzer
from App.Analysis.hierarchical.behaviour import behaviour_H_analyzer
from App.Analysis.hierarchical.address import address_H_analyzer
from App.Core.normalizer import URLNormalizer

test_url=[
    "http://google.com-support-account:secureUpdate2024@192.168.1.55:8080/login/index.php",
    "https://www.paypal.com.verify.cgi-bin.webscr.cmd-login-submit.dispatch.588214.xyz/secure/auth.html",
    "https://service-admin.net/files/%2e%2e%2fconfig.ini?redirect=http%3A%2F%2Fevil.com&token=AeB4%3D%3D",
    "http://142.250.190.46/search",
    "http://10.0.0.138/admin/config",
    "http://127.0.0.1/phpmyadmin",
    "http://45.22.19.12:6667/payload.bin",
    "http://[2001:db8::1]:8080/auth",
    "http://192.168.1.1.banque-secure.com/login",
    "https://1.1.1.1/dns-query"
]
for url in test_url:
    Normal=URLNormalizer(url)
    Nurl=Normal.normalize_url()
    h=HierarchicalParser(Nurl)
    parsed=h.data()
    a1=address_H_analyzer(parsed)
    a2=lexical_H_analyzer(parsed)
    a3=behaviour_H_analyzer(parsed)
    print(f"data parsee: \n {parsed}")
    print(f"analyse d'addresse \n {a1.analyze()}")
    print(f"analyse lexique \n {a2.analyze()}")
    print(f"analyse de comportement \n {a3.analyze()}")
    print("")
    print("")

