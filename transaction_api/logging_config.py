"""Configuration du logging pour l'API Transaction.

Ce module fournit la configuration centralisée du logging pour l'API Transaction,
en configurant à la fois les gestionnaires de console et de fichier avec un formatage cohérent.

Fonctions
---------
setup_logging()
    Configurer le logging pour l'ensemble de l'application.
get_logger(name)
    Obtenir une instance de logger pour un module spécifique.
"""

import logging
import logging.config
from typing import Dict, Any

from transaction_api.config import LOG_LEVEL, LOG_FORMAT


def setup_logging() -> None:
    """Configurer le logging.
    
    Configure le logging avec à la fois des gestionnaires de console et de fichier
    en utilisant les paramètres du module de configuration. Crée un fichier de log
    à 'transaction_api.log' et diffuse les logs sur la console avec un formatage cohérent.
    
    Retours
    -------
    None
    
    Exemples
    --------
    >>> setup_logging()
    >>> logger = get_logger(__name__)
    >>> logger.info("Application démarrée")
    """
    logging_config: Dict[str, Any] = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "standard": {
                "format": LOG_FORMAT,
            },
        },
        "handlers": {
            "default": {
                "level": LOG_LEVEL,
                "class": "logging.StreamHandler",
                "formatter": "standard",
            },
            "file": {
                "level": LOG_LEVEL,
                "class": "logging.FileHandler",
                "filename": "transaction_api.log",
                "formatter": "standard",
            },
        },
        "loggers": {
            "": {
                "handlers": ["default", "file"],
                "level": LOG_LEVEL,
                "propagate": True,
            },
        },
    }
    logging.config.dictConfig(logging_config)


def get_logger(name: str) -> logging.Logger:
    """Obtenir une instance de logger.
    
    Retourne une instance de logger pour le nom de module spécifié. Le logger est
    configuré avec les paramètres établis par setup_logging().
    
    Paramètres
    ----------
    name : str
        Le nom du logger, généralement le nom du module (__name__).
    
    Retours
    -------
    logging.Logger
        Une instance de logger configurée pour le nom spécifié.
    
    Exemples
    --------
    >>> logger = get_logger(__name__)
    >>> logger.debug("Message de débogage")
    >>> logger.info("Message d'information")
    >>> logger.error("Message d'erreur")
    """
    return logging.getLogger(name)
