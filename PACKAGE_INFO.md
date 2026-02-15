# Information sur le Package Transaction API

## Vue d'ensemble

Le package `transaction-api` est une application FastAPI complète pour l'analyse des transactions, la détection de fraude et les informations sur les clients. Il est conçu pour être installable en tant que module Python standard.

## Structure du Package

```
transaction-api/
├── transaction_api/                   # Package principal
│   ├── __init__.py                    # Exports publics du package
│   ├── main.py                        # Application FastAPI principale
│   ├── models.py                      # Modèles de données Pydantic
│   ├── repository.py                  # Couche d'accès aux données
│   ├── pagination.py                  # Services de pagination
│   ├── exceptions.py                  # Exceptions personnalisées
│   ├── config.py                      # Configuration de l'application
│   ├── logging_config.py              # Configuration de la journalisation
│   ├── app_context.py                 # Contexte global de l'application
│   ├── routes/                        # Gestionnaires de routes API
│   │   ├── __init__.py
│   │   ├── transaction_routes.py      # Routes des transactions
│   │   ├── customer_routes.py         # Routes des clients
│   │   ├── fraud_routes.py            # Routes de détection de fraude
│   │   ├── statistics_routes.py       # Routes des statistiques
│   │   └── system_routes.py           # Routes système
│   └── services/                      # Services métier
│       ├── __init__.py
│       ├── transaction_service.py     # Service des transactions
│       ├── customer_service.py        # Service des clients
│       ├── fraud_service.py           # Service de détection de fraude
│       ├── statistics_service.py      # Service des statistiques
│       └── health_service.py          # Service de santé
├── tests/                             # Tests du projet
│   ├── unit/                          # Tests unitaires
│   ├── integration/                   # Tests d'intégration
│   ├── properties/                    # Tests basés sur les propriétés
│   └── conftest.py                    # Configuration pytest
├── data/                              # Données de test
│   └── transactions.csv               # Fichier de données de test
├── streamlit_app                      # Application Streamlit du projet
|   └── app.py                         # Interface Streamlit
├── setup.py                           # Configuration setuptools
├── pyproject.toml                     # Configuration moderne du projet
├── MANIFEST.in                        # Fichiers à inclure dans le package
├── tox.ini                            # Configuration tox pour les tests
├── Makefile                           # Commandes courantes
├── requirements.txt                   # Dépendances du projet
├── LICENSE                            # Licence MIT
├── README.md                          # Documentation principale
├── INSTALLATION.md                    # Guide d'installation
└── PACKAGE_INFO.md                    # Ce fichier
```

## Modules Principaux

### transaction_api.main
L'application FastAPI principale avec tous les gestionnaires d'exceptions et la configuration du cycle de vie.

**Exports:**
- `app`: Instance FastAPI

### transaction_api.models
Modèles de données Pydantic pour les requêtes et réponses de l'API.

**Classes principales:**
- `Transaction`: Modèle de transaction
- `SearchFilters`: Filtres de recherche
- `PaginatedResponse`: Réponse paginée générique
- `OverviewStats`: Statistiques d'aperçu
- `FraudSummary`: Résumé de fraude

### transaction_api.repository
Couche d'accès aux données avec indexation et recherche.

**Classes principales:**
- `TransactionRepository`: Référentiel de transactions

### transaction_api.pagination
Services de pagination pour les réponses paginées.

**Classes principales:**
- `PaginationService`: Service de pagination

### transaction_api.services
Services métier pour la logique applicative.

**Modules:**
- `transaction_service.py`: Logique des transactions
- `customer_service.py`: Logique des clients
- `fraud_service.py`: Logique de détection de fraude
- `statistics_service.py`: Logique des statistiques
- `health_service.py`: Logique de santé du système

### transaction_api.routes
Gestionnaires de routes API organisés par domaine.

**Modules:**
- `transaction_routes.py`: Routes des transactions
- `customer_routes.py`: Routes des clients
- `fraud_routes.py`: Routes de fraude
- `statistics_routes.py`: Routes des statistiques
- `system_routes.py`: Routes système

## Installation

### Installation de base
```bash
pip install -e .
```

### Installation avec développement
```bash
pip install -e ".[dev]"
```

### Installation avec interface utilisateur
```bash
pip install -e ".[ui]"
```

### Installation complète
```bash
pip install -e ".[dev,ui]"
```

## Utilisation

### Démarrer l'API
```bash
# Utiliser la commande console
transaction-api

# Ou utiliser uvicorn directement
uvicorn transaction_api.main:app --reload
```

### Utiliser le module dans votre code
```python
from transaction_api import app, TransactionRepository, Transaction

# Accéder à l'application
print(app)

# Créer une instance du référentiel
repo = TransactionRepository()
repo.load_from_csv("data/transactions.csv")

# Récupérer les transactions
transactions = repo.get_all_transactions()
```

### Lancer l'interface Streamlit
```bash
streamlit run streamlit_app/app.py
```

## Dépendances

### Dépendances principales
- `fastapi`: Framework web
- `uvicorn`: Serveur ASGI
- `pydantic`: Validation de données
- `pandas`: Manipulation de données
- `numpy`: Calculs numériques

### Dépendances de développement
- `pytest`: Framework de test
- `hypothesis`: Tests basés sur les propriétés
- `black`: Formatage de code
- `flake8`: Vérification de qualité
- `mypy`: Vérification de types

### Dépendances optionnelles (UI)
- `streamlit`: Interface utilisateur
- `plotly`: Visualisations
- `requests`: Requêtes HTTP

## Configuration

### Variables d'environnement
- `API_BASE_URL`: URL de base de l'API (défaut: http://localhost:8000/api)
- `LOG_LEVEL`: Niveau de journalisation (défaut: INFO)

### Fichiers de configuration
- `transaction_api/config.py`: Configuration de l'application
- `transaction_api/logging_config.py`: Configuration de la journalisation

## Tests

### Exécuter tous les tests
```bash
pytest
```

### Exécuter avec couverture
```bash
pytest tests/ -v --cov
```


## Documentation

La documentation complète est disponible dans:
- `README.md`: Vue d'ensemble du projet
- `INSTALLATION.md`: Guide d'installation détaillé
- Docstrings NumPyDoc dans le code source

## Versioning

Le projet suit le versioning sémantique (SemVer):
- Version actuelle: 1.0.0
- Format: MAJOR.MINOR.PATCH

## Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## Auteurs

- Christian SONTSA
- Stéphane NZATI
- Brenda Camélia Sama

## Support

Pour toute question ou problème:
1. Consultez la documentation
2. Vérifiez les issues existantes
3. Créez une nouvelle issue si nécessaire

## Contribution

Les contributions sont bienvenues! Veuillez:
1. Fork le projet
2. Créer une branche pour votre fonctionnalité
3. Commiter vos changements
4. Pousser vers la branche
5. Créer une Pull Request