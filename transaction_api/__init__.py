"""Paquet API Transaction.

Une application FastAPI haute performance pour l'analyse de transactions, la détection
de fraude et les informations sur les clients. Fournit des points de terminaison REST
complets pour interroger les données de transaction avec des capacités avancées de
filtrage, pagination et analyse statistique.

Modules
-------
main
    Configuration et mise en place de l'application FastAPI.
models
    Modèles de données Pydantic pour les requêtes et réponses de l'API.
repository
    Couche d'accès aux données pour la gestion des transactions.
pagination
    Utilitaires et services de pagination.
exceptions
    Classes d'exception personnalisées.
config
    Constantes de configuration et paramètres.
logging_config
    Configuration de la journalisation et utilitaires.
app_context
    Gestion du contexte global de l'application.
routes
    Gestionnaires de routes API organisés par fonctionnalité.
services
    Services de logique métier.

Exports Publics
---------------
__version__ : str
    Version du paquet.
__author__ : str
    Auteurs du paquet.
app : FastAPI
    Instance de l'application FastAPI.
TransactionRepository : class
    Classe du référentiel de transactions.
"""

__version__ = "1.0.0"
__author__ = "Christian SONTSA, Stéphane NZATI, Brenda Camélia Sama"
__all__ = [
    "app",
    "TransactionRepository",
    "PaginationService",
    "Transaction",
    "SearchFilters",
]

from transaction_api.main import app
from transaction_api.repository import TransactionRepository
from transaction_api.pagination import PaginationService
from transaction_api.models import Transaction, SearchFilters
