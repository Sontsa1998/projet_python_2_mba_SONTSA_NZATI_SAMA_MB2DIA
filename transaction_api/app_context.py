"""Contexte global de l'application.

Ce module gère le contexte global de l'application, y compris l'instance singleton
du TransactionRepository qui est partagée dans toute l'application.

Attributs
---------
repository : Optional[TransactionRepository]
    Instance globale du TransactionRepository. Initialisée lors du démarrage de l'application
    et utilisée tout au long du cycle de vie de l'application.
"""

from typing import Optional

from transaction_api.repository import TransactionRepository

# Global repository instance
repository: Optional[TransactionRepository] = None