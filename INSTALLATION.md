# Guide d'Installation - Transaction API

Ce guide explique comment installer et utiliser le module `transaction-api` en tant que package Python installable.

## Prérequis

- Python 3.10 ou supérieur
- pip (gestionnaire de paquets Python)
- virtualenv (recommandé)

## Installation

### 1. Installation depuis le répertoire local

Pour installer le package depuis le répertoire du projet:

```bash
# Naviguer vers le répertoire du projet
cd /chemin/vers/transaction-api

# Installation en mode développement (editable)
pip install -e .

# Ou installation standard
pip install .
```

### 2. Installation avec les dépendances de développement

Pour installer le package avec les outils de développement:

```bash
pip install -e ".[dev]"
```

### 3. Installation avec l'interface utilisateur Streamlit

Pour installer le package avec les dépendances de l'interface utilisateur:

```bash
pip install -e ".[ui]"
```

### 4. Installation complète (dev + ui)

```bash
pip install -e ".[dev,ui]"
```

## Utilisation

### Démarrer l'API

Après installation, vous pouvez démarrer l'API de plusieurs façons:

#### Option 1: Utiliser la commande console

```bash
transaction-api
```

#### Option 2: Utiliser Python directement

```bash
python -m transaction_api.main
```

#### Option 3: Utiliser uvicorn

```bash
uvicorn transaction_api.main:app --reload --host 0.0.0.0 --port 8000
```

### Utiliser le module dans votre code

```python
from transaction_api import app, TransactionRepository, Transaction

# Accéder à l'application FastAPI
print(app)

# Créer une instance du référentiel
repo = TransactionRepository()
repo.load_from_csv("data/transactions.csv")

# Récupérer toutes les transactions
transactions = repo.get_all_transactions()
```

### Lancer l'interface Streamlit

```bash
streamlit run app.py
```

## Vérification de l'installation

Pour vérifier que le package est correctement installé:

```bash
# Vérifier la version
python -c "import transaction_api; print(transaction_api.__version__)"

# Vérifier les modules disponibles
python -c "from transaction_api import app, TransactionRepository; print('Installation réussie!')"
```

## Désinstallation

Pour désinstaller le package:

```bash
pip uninstall transaction-api
```

## Dépannage

### Erreur: "No module named 'transaction_api'"

Assurez-vous que le package est correctement installé:
```bash
pip list | grep transaction-api
```

### Erreur: "Port 8000 already in use"

Utilisez un port différent:
```bash
uvicorn transaction_api.main:app --port 8001
```

### Erreur: "CSV file not found"

Assurez-vous que le fichier `data/transactions.csv` existe dans le répertoire courant.

## Structure du Package

```
transaction-api/
├── transaction_api/
│   ├── __init__.py           # Exports publics du package
│   ├── main.py               # Application FastAPI
│   ├── models.py             # Modèles Pydantic
│   ├── repository.py         # Couche d'accès aux données
│   ├── pagination.py         # Services de pagination
│   ├── exceptions.py         # Exceptions personnalisées
│   ├── config.py             # Configuration
│   ├── logging_config.py     # Configuration de la journalisation
│   ├── app_context.py        # Contexte global
│   ├── routes/               # Gestionnaires de routes
│   └── services/             # Services métier
├── tests/                    # Tests unitaires et propriétés
├── data/                     # Données de test
├── setup.py                  # Configuration setuptools
├── pyproject.toml            # Configuration moderne du projet
├── MANIFEST.in               # Fichiers à inclure dans le package
├── requirements.txt          # Dépendances du projet
├── LICENSE                   # Licence MIT
└── README.md                 # Documentation du projet
```

## Développement

### Installer en mode éditable

```bash
pip install -e ".[dev]"
```

### Exécuter les tests

```bash
pytest
```

### Exécuter les tests avec couverture

```bash
pytest --cov=transaction_api --cov-report=html
```

### Formater le code

```bash
black transaction_api tests
isort transaction_api tests
```

### Vérifier la qualité du code

```bash
flake8 transaction_api tests
mypy transaction_api
```

## Support

Pour toute question ou problème, veuillez consulter la documentation ou créer une issue sur le dépôt GitHub.
