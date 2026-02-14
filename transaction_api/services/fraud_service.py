"""Fraud detection service for business logic."""

from typing import List

from transaction_api.logging_config import get_logger
from transaction_api.models import (
    FraudPrediction,
    FraudSummary,
    FraudTypeStats,
    Transaction,
)
from transaction_api.repository import TransactionRepository

logger = get_logger(__name__)


class FraudService:
    """Service for fraud detection operations."""

    def __init__(self, repository: TransactionRepository) -> None:
        """Initialize the service."""
        self.repository = repository
