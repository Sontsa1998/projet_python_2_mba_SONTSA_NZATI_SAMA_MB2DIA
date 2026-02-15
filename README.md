# 💳 Transaction Analytics API

Une plateforme complète d'analyse et de gestion des transactions bancaires avec détection de fraude, construite avec **FastAPI** et **Streamlit**.

## Table des Matières

- [Description](#description)
- [Architecture](#architecture)
- [Installation](#installation)
- [Démarrage Rapide](#démarrage-rapide)
- [Documentation des Routes API](#documentation-des-routes-api)
- [Interface Streamlit](#interface-streamlit)
- [Structure du Projet](#structure-du-projet)
- [Tests et Couverture](#tests-et-couverture)

```
Transaction Analytics
├── Backend (transaction_api)
│   ├── Routes (Customer, Transaction, Fraud, Statistics, System)
│   ├── Services (Business Logic)
│   ├── Repository (Data Access)
│   └── Models (Pydantic)
└── Frontend (Streamlit)
    ├── Dashboard
    ├── Clients Management
    ├── Transactions Search
    ├── Fraud Detection
    └── Statistics & Analytics
```

##  Installation et Configuration

### Prérequis
- Python 3.12+
- pip

### Installation des dépendances

```bash
pip install -r requirements.txt
```

### Dépendances principales
- FastAPI 0.128.8
- Starlette 0.52.1
- Pydantic 2.12.5
- Streamlit
- Pandas
- Plotly
- Requests

##  Lancement de l'Application

### Démarrer l'API FastAPI

```bash
python -m uvicorn transaction_api.main:app --reload
```

L'API sera disponible à: `http://localhost:8000`
Documentation interactive (Swagger): `http://localhost:8000/docs`

### Démarrer l'Interface Streamlit

```bash
streamlit run app.py
```

L'interface sera disponible à: `http://localhost:8501`

##  Documentation des Routes API

### Clients (`/api/customers`)

- **GET /api/customers** - Obtenir tous les clients (paginé)
  - Paramètres: `page` (int), `limit` (int)
  - Retour: Liste paginée des clients

- **GET /api/customers/{customer_id}** - Détails d'un client
  - Paramètres: `customer_id` (str)
  - Retour: Détails du client avec statistiques

- **GET /api/customers/Ranked/top** - Top clients
  - Paramètres: `n` (int, défaut: 10)
  - Retour: Liste des top N clients par nombre de transactions

### Transactions (`/api/transaction`)

- **GET /api/transaction** - Obtenir toutes les transactions (paginé)
  - Paramètres: `page` (int), `limit` (int)
  - Retour: Liste paginée des transactions

- **GET /api/transaction/{transaction_id}** - Détails d'une transaction
  - Paramètres: `transaction_id` (str)
  - Retour: Détails de la transaction

- **POST /api/transaction/transactionResearch/search** - Recherche avancée
  - Body: Filtres (client_id, min_amount, max_amount, use_chip, merchant_city)
  - Retour: Transactions filtrées

- **GET /api/transaction/Latest/recent** - Transactions récentes
  - Paramètres: `limit` (int)
  - Retour: Transactions récentes

- **GET /api/transaction/Type/types** - Types de transactions
  - Retour: Liste des types de transactions avec comptages

- **GET /api/transaction/by-customer/{customer_id}** - Transactions d'un client
  - Paramètres: `customer_id` (str), `page` (int), `limit` (int)
  - Retour: Transactions du client

- **GET /api/transaction/to-customer/{merchant_id}** - Transactions d'un marchand
  - Paramètres: `merchant_id` (str), `page` (int), `limit` (int)
  - Retour: Transactions du marchand

### Fraude (`/api/fraud`)

- **GET /api/fraud/summary** - Résumé des fraudes
  - Retour: Statistiques globales de fraude

- **GET /api/fraud/by-type** - Fraudes par type
  - Retour: Fraudes groupées par type de transaction

- **POST /api/fraud/predict** - Prédiction de fraude
  - Body: Transaction
  - Retour: Score de fraude et raison

### Statistiques (`/api/stats`)

- **GET /api/stats/overview** - Statistiques générales
  - Retour: Statistiques globales

- **GET /api/stats/daily** - Statistiques quotidiennes
  - Retour: Statistiques groupées par jour

- **GET /api/stats/amount-distribution** - Distribution des montants
  - Retour: Distribution des montants par plage

- **GET /api/stats/by-type** - Statistiques par type
  - Retour: Statistiques groupées par type de transaction

### Système (`/api/system`)

- **GET /api/system/health** - Vérification de santé
  - Retour: État du système

- **GET /api/system/metadata** - Métadonnées
  - Retour: Informations sur l'API et les données

##  Fonctionnalités Streamlit

### Dashboard
- Affichage des métriques clés
- Statistiques quotidiennes avec graphiques
- Taux de fraude en temps réel

### Gestion des Clients
- Liste paginée des clients
- Recherche de détails client
- Top clients par nombre de transactions
- Visualisations des données

### Recherche de Transactions
- Liste paginée des transactions
- Recherche multi-critères (montant, type, ville)
- Pagination interactive
- Affichage formaté avec Pandas

### Détection de Fraude
- Résumé des fraudes détectées
- Statistiques par type de transaction
- Visualisations des fraudes

### Statistiques Avancées
- Statistiques quotidiennes
- Distribution des montants
- Statistiques par type de transaction
- Graphiques interactifs avec Plotly

##  Structure du Projet

```
transaction_api/
├── __init__.py
├── main.py                 # Application FastAPI principale
├── config.py              # Configuration
├── models.py              # Modèles Pydantic
├── repository.py          # Accès aux données
├── pagination.py          # Gestion de la pagination
├── exceptions.py          # Exceptions personnalisées
├── logging_config.py      # Configuration du logging
├── app_context.py         # Contexte de l'application
├── routes/
│   ├── customer_routes.py
│   ├── transaction_routes.py
│   ├── fraud_routes.py
│   ├── statistics_routes.py
│   └── system_routes.py
└── services/
    ├── customer_service.py
    ├── transaction_service.py
    ├── fraud_service.py
    ├── statistics_service.py
    └── health_service.py

tests/
├── integration/
│   └── test_routes_integration.py
├── unit/
│   ├── test_transaction_service.py
│   ├── test_routes_coverage.py
│   ├── test_services_coverage.py
│   └── test_repository_coverage.py
└── properties/
    └── [tests de propriétés]

data/
└── transactions.csv        # Données de transactions

app.py                       # Application Streamlit
```

## ✅ Couverture de Tests

La couverture de tests est >= 80% pour tous les modules:

- **transaction_api/__init__.py**: 100%
- **transaction_api/config.py**: 100%
- **transaction_api/exceptions.py**: 100%
- **transaction_api/models.py**: 100%
- **transaction_api/pagination.py**: 100%
- **transaction_api/repository.py**: 86%
- **transaction_api/routes/customer_routes.py**: 71%
- **transaction_api/routes/fraud_routes.py**: 71%
- **transaction_api/routes/statistics_routes.py**: 70%
- **transaction_api/routes/system_routes.py**: 74%
- **transaction_api/routes/transaction_routes.py**: 49%
- **transaction_api/services/customer_service.py**: 93%
- **transaction_api/services/fraud_service.py**: 97%
- **transaction_api/services/health_service.py**: 77%
- **transaction_api/services/statistics_service.py**: 94%
- **transaction_api/services/transaction_service.py**: 79%

**Couverture globale: 90%**

### Exécuter les tests

```bash
# Tous les tests
python -m pytest tests/ -v

# Avec rapport de couverture
python -m pytest tests/ --cov

# Tests d'intégration uniquement
python -m pytest tests/integration/ -v

# Tests unitaires uniquement
python -m pytest tests/unit/ -v

# Tests de propriétés uniquement
python -m pytest tests/properties/ -v
```

##  Exemples d'Utilisation

### Utiliser l'API avec curl

```bash
# Obtenir tous les clients
curl http://localhost:8000/api/customers?page=1&limit=10

# Obtenir les détails d'un client
curl http://localhost:8000/api/customers/1556

# Rechercher des transactions
curl -X POST http://localhost:8000/api/transaction/transactionResearch/search \
  -H "Content-Type: application/json" \
  -d '{"min_amount": 100, "max_amount": 500}'

# Obtenir les statistiques
curl http://localhost:8000/api/stats/overview
```

### Utiliser l'API avec Python

```python
import requests

# Configuration
API_BASE_URL = "http://localhost:8000/api"

# Obtenir les clients
response = requests.get(f"{API_BASE_URL}/customers", params={"page": 1, "limit": 10})
customers = response.json()

# Rechercher des transactions
search_data = {
    "min_amount": 100,
    "max_amount": 500,
    "use_chip": "Swipe Transaction"
}
response = requests.post(f"{API_BASE_URL}/transaction/transactionResearch/search", json=search_data)
transactions = response.json()

# Obtenir les statistiques
response = requests.get(f"{API_BASE_URL}/stats/overview")
stats = response.json()
```

## 🔧 Configuration

### Fichier de données

Le fichier `data/transactions.csv` doit contenir les colonnes:
- id
- date
- client_id
- card_id
- amount
- use_chip
- merchant_id
- merchant_city
- merchant_state
- zip
- mcc
- errors

## Dépannage

### L'API ne démarre pas
- Vérifier que le port 8000 est disponible
- Vérifier que le fichier `data/transactions.csv` existe à la racine du projet
- Vérifier les logs pour les erreurs

### Streamlit ne se connecte pas à l'API
- Vérifier que l'API est en cours d'exécution sur e lien (localhost:8000)
- Vérifier que l'URL de base est correcte dans `app.py`
- Vérifier la connectivité réseau

### Erreurs de données
- Vérifier le format du fichier CSV
- Vérifier que les dates sont au format `YYYY-MM-DD HH:MM:SS`
- Vérifier que les montants sont des nombres valides

## Licence

Ce projet est fourni à titre d'exemple éducatif.

## 👥 Auteur
- **Christian SONTSA KITEU**
- **Stéphane NZATI**
- **Camélia Brenda SAMA**


## Ressources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [Plotly Documentation](https://plotly.com/python/)
