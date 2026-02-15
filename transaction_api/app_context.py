"""Global application context.

This module manages the global application context, including the singleton
instance of the TransactionRepository that is shared across the application.

Attributes
----------
repository : Optional[TransactionRepository]
    Global instance of the TransactionRepository. Initialized during application
    startup and used throughout the application lifecycle.
"""

from typing import Optional

from transaction_api.repository import TransactionRepository

# Global repository instance
repository: Optional[TransactionRepository] = None