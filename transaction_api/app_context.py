"""Global application context."""

from typing import Optional

from transaction_api.repository import TransactionRepository

# Global repository instance
repository: Optional[TransactionRepository] = None