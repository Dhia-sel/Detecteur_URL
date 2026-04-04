Projet-Detecteur-Url/
│
├── README.md
├── requirements.txt
│
├── App/
│   ├── main.py
│
│   ├── Core/
│   │   ├── classifier.py
│   │   ├── normalizer.py
│   │   ├── constants.py
│   │   ├── pipeline.py
│   │   └── __pycache__/
│
│   ├── Parsers/
│   │   ├── base.py
│   │   ├── hierarchical.py
│   │   ├── embedded.py
│   │   ├── nested.py
│   │   ├── opaque.py
│   │   └── __pycache__/
│
│   ├── Analysis/
│   │   ├── rules.py
│   │   ├── embedded/
│   │   │   ├── behaviour.py
│   │   │   ├── lexical.py
│   │   │   └── __pycache__/
│   │   ├── hierarchical/
│   │   │   ├── address.py
│   │   │   ├── behaviour.py
│   │   │   ├── lexical.py
│   │   │   └── __pycache__/
│   │   ├── nested/
│   │   │   ├── behaviour.py
│   │   │   ├── lexical.py
│   │   │   └── __pycache__/
│   │   └── opac/
│   │       ├── behaviour.py
│   │       ├── lexical.py
│   │       └── __pycache__/
│
│   ├── Explaining/
│   │   ├── formatter.py
│   │   └── messages.py
│
│   ├── MachineLearning/
│   └── Utils/
│
├── Docs/
│   └── architecture.md
│
└── Tests/
    ├── embedded_test.py
    ├── hierarchical_test.py
    ├── nested_test.py
    └── opac_test.py
    ├── architecture.md
    ├── ml_design.md
    └── examples.md
