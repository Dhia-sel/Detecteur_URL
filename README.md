# Détecteur d’URL – Analyse de phishing

Projet Python pour analyser et classer des URLs suspectes à l’aide d’une combinaison d’analyses heuristiques, d’extraction de features, et d’un modèle de machine learning.

Le système vise à détecter les liens potentiellement malveillants, à expliquer le verdict et à exposer les résultats via une API REST.

## Fonctionnalités

- Normalisation et classification des URLs
- Analyse de structure et de composants de l’URL
- Règles heuristiques pour repérer les signaux de phishing
- Modèle ML basé sur des features d’URL
- API FastAPI pour effectuer des scans
- Interface web légère en HTML/JavaScript
- Rapport d’explication et de score de risque

## Stack technique

- Python
- FastAPI
- scikit-learn
- pandas / numpy
- joblib
- HTML + JavaScript

## Structure du projet

```text
Projet-Detecteur-Url/
├── API/
│   ├── routes/
│   ├── schema/
│   └── server.py
├── App/
│   ├── Analysis/
│   ├── Core/
│   ├── Explaining/
│   ├── MachineLearning/
│   ├── Parsers/
│   ├── Utils/
│   └── main.py
├── Docs/
│   └── architecture.md
├── Frontend/
│   ├── css/
│   ├── js/
│   └── index.html
├── ML/
│   ├── datasets/
│   ├── download_training_datasets.py
│   ├── phishing_model.py
│   ├── phishing_model.joblib
│   └── ...
├── Tests/
├── requirements.txt
├── README.md
└── ...
```

## Prérequis

- Python 3.10+
- pip
- Accès internet pour télécharger les datasets optionnels du modèle ML

## Installation

1. Cloner le dépôt :

```bash
git clone https://github.com/<votre-utilisateur>/Projet-Detecteur-Url.git
cd Projet-Detecteur-Url
```

2. Créer un environnement virtuel :

```bash
python -m venv .venv
```

3. Activer l’environnement :

Sous Windows (PowerShell) :

```powershell
.\.venv\Scripts\Activate.ps1
```

Sous Linux/macOS :

```bash
source .venv/bin/activate
```

4. Installer les dépendances :

```bash
pip install -r requirements.txt
```

## Lancement de l’API

Depuis la racine du projet :

```bash
uvicorn API.server:app --host 0.0.0.0 --port 8000 --reload
```

Ensuite, la documentation Swagger est disponible à :

```text
http://localhost:8000/docs
```

## Exemple d’appel API

### Scan d’une URL

```bash
curl -X POST "http://localhost:8000/api/scan" \
  -H "Content-Type: application/json" \
  -d '{"url":"https://example.com/login"}'
```

La réponse contient notamment :

- l’URL analysée
- le type de URL
- le rapport d’analyse
- le résultat ML
- le score de risque et la conclusion

## Modèle ML

Le modèle est géré dans le dossier `ML/`.

Si le modèle n’existe pas encore, le système peut le générer automatiquement lors du premier scan. Pour précharger les datasets de formation :

```bash
python ML/download_training_datasets.py
```

Puis vous pouvez lancer l’entraînement ou laisser l’API le faire automatiquement lors d’un premier scan.

## Interface web

Le front simple est présent dans le dossier `Frontend/`.

Vous pouvez le lancer localement avec :

```bash
python -m http.server 8080 --directory Frontend
```

Puis ouvrir :

```text
http://localhost:8080/
```

## Tests

Pour exécuter les tests du projet :

```bash
pytest
```

## Notes

- Le projet combine analyse logique et apprentissage automatique.
- L’API est le point d’entrée principal pour les intégrations.
- Les fichiers d’architecture et de documentation dans `Docs/` permettent de comprendre les composants analytiques.

## Licence

Le dépôt n’indique pas de licence spécifique dans le code source actuel. Vérifiez bien la politique de distribution avant une mise en production ou un partage externe.
