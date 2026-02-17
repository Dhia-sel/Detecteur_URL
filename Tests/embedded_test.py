import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
parent_dir1 = os.path.dirname(parent_dir)
src_path = os.path.join(parent_dir1, 'Projet-Detecteur-Url')
sys.path.append(src_path)

from App.Parsers.embedded import EmbeddedParser
from App.Analysis.embedded.lexical import lexical_E_analyzer
from App.Analysis.embedded.behaviour import behaviour_E_analyzer
from App.Core.normalizer import URLNormalizer


test_urls =[
    "data:text/html;base64,PGh0bWw+PHNjcmlwdD5hbGVydCgnWW91IGhhdmUgYmVlbiBoYWNrZWQnKTs8L3NjcmlwdD48L2h0bWw+",
    "data:text/javascript,alert('XSS_ATTACK_DETECTED')",
    "data:application/x-javascript;base64,ZXZhbChhdG9iKCdhbGVydChkb2N1bWVudC5jb29raWUpJykpOw==",
    "data:image/png;base64,PHNjcmlwdD5kb2N1bWVudC5sb2NhdGlvbj0naHR0cDovL2V2aWwuY29tJzwvc2NyaXB0Pg==",
    "data:text/html,<form action='http://phishing.com'><input type='password' name='pass'></form>",
    "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciPjxzY3JpcHQ+YWxlcnQoMSk8L3NjcmlwdD48L3N2Zz4=",
    "data:text/plain;charset=utf-8,Juste%20du%20texte%20inoffensif%20pour%20le%20test",
    "data:application/octet-stream;base64,TVqQAAMAAAAEAAAA//8AALgAAAAAAAAAQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA=",
    "data:text/xml;base64,PCFET0NUWVBFIGZvbyBbPCFFTlRJVFkgeHhlIFNZU1RFTSAiZmlsZTovLy9ldGMvcGFzc3dkIj5dPjxmb28+Jnh4ZTs8L2Zvbz4=",
    "data:text/html,aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
]

for url in test_urls:
    normal=URLNormalizer(url)
    Nurl=normal.normalize_url()
    e=EmbeddedParser(Nurl)
    parsed=e.data()
    print(f"donnees parsees :\n {parsed}")
    a1=lexical_E_analyzer(parsed)
    a2=behaviour_E_analyzer(parsed)
    print(f"analyse lexique :\n {a1.analyze()}")
    print(f"analyse de comportement:\n {a2.analyze()}")
    print("")
    print("")
