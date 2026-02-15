"""Configuration et constantes pour l'API Transaction.

Ce module fournit les paramètres de configuration centralisés pour l'API Transaction,
y compris les métadonnées de l'API, les chemins de données, les limites de pagination,
les seuils de performance et la configuration du logging.

Attributs
---------
API_VERSION : str
    La version actuelle de l'API Transaction.
API_TITLE : str
    Le titre de l'API Transaction.
API_DESCRIPTION : str
    Une brève description du but de l'API Transaction.
CSV_FILE_PATH : str
    Chemin d'accès au fichier CSV contenant les données de transactions.
CHUNK_SIZE : int
    Nombre de lignes à lire à la fois lors du traitement des données CSV.
DEFAULT_LIMIT : int
    Nombre par défaut d'éléments à retourner dans les réponses paginées.
MAX_LIMIT : int
    Nombre maximum d'éléments autorisés dans une seule réponse paginée.
MIN_LIMIT : int
    Nombre minimum d'éléments autorisés dans une réponse paginée.
RESPONSE_TIME_THRESHOLD_MS : float
    Seuil en millisecondes pour les temps de réponse normaux.
COMPLEX_QUERY_THRESHOLD_MS : float
    Seuil en millisecondes pour les temps de réponse des requêtes complexes.
AMOUNT_BUCKETS : list
    Liste de dictionnaires définissant les plages de distribution des montants de transactions.
LOG_LEVEL : str
    Niveau de logging pour l'application (DEBUG, INFO, WARNING, ERROR, CRITICAL).
LOG_FORMAT : str
    Chaîne de format pour les messages de log.
"""

import os
from typing import Final

# API Configuration
API_VERSION: Final[str] = "1.0.0"
API_TITLE: Final[str] = "Transaction API"
API_DESCRIPTION: Final[str] = "High-performance API for transaction analysis"

# Data Configuration
CSV_FILE_PATH: Final[str] = os.getenv("CSV_FILE_PATH", "data/transactions.csv")
CHUNK_SIZE: Final[int] = 10000  # Number of rows to read at a time

# Pagination Configuration
DEFAULT_LIMIT: Final[int] = 50
MAX_LIMIT: Final[int] = 1000
MIN_LIMIT: Final[int] = 1

# Performance Configuration
RESPONSE_TIME_THRESHOLD_MS: Final[float] = 500.0
COMPLEX_QUERY_THRESHOLD_MS: Final[float] = 1000.0

# Amount Distribution Buckets
AMOUNT_BUCKETS: Final[list] = [
    {"min": 0, "max": 100, "label": "0-100"},
    {"min": 100, "max": 500, "label": "100-500"},
    {"min": 500, "max": 1000, "label": "500-1000"},
    {"min": 1000, "max": float("inf"), "label": "1000+"},
]

# Logging Configuration
LOG_LEVEL: Final[str] = os.getenv("LOG_LEVEL", "INFO")
LOG_FORMAT: Final[str] = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
