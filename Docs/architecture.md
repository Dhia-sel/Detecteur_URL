Projet-Detecteur-Url/
│
├── README.md
├── requirements.txt
├── .gitignore
│
├── App/
│   ├── main.py
│
│   ├── Core/
│   │   ├── classifier.py        
│   │   ├── normalizer.py
│   │   └── constants.py
│
│   ├── Parsers/
│   │   ├── base.py
│   │   ├── hierarchical.py
│   │   ├── embedded.py
│   │   ├── nested.py
│   │   ├── opaque.py
│   │   └── relative.py
│
│   ├── Analysis/
│   │   ├── address_analysis.py
│   │   ├── lexical_analysis.py
│   │   ├── behavioral_analysis.py
│   │   └── risk_rules.py
│
│   ├── ML/
│   │   ├── feature_builder.py   
│   │   ├── model.py        
│   │   ├── predict.py        
│   │   └── datasets/
│   │       └── phishing_urls.csv
│
│   ├── Explain/
│   │   ├── formatter.py
│   │   └── messages.py
│
│   └── Utils/
│       ├── ip_utils.py
│       ├── domain_utils.py
│       └── string_utils.py
│
├── Tests/
│   ├── test_classifier.py
│   ├── test_parsers.py
│   ├── test_ml.py
│   └── test_pipeline.py
│
└── Docs/
    ├── architecture.md
    ├── ml_design.md
    └── examples.md
