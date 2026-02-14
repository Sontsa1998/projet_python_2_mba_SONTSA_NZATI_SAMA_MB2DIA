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

    def get_fraud_summary(self) -> FraudSummary:
        """Get fraud detection summary."""
        transactions = self.repository.get_all_transactions()
        fraud_transactions = self.repository.get_fraud_transactions()

        total_count = len(transactions)
        fraud_count = len(fraud_transactions)
        if total_count > 0:
            fraud_rate = fraud_count / total_count
        else:
            fraud_rate = 0.0
        total_fraud_amount = sum(t.amount for t in fraud_transactions)

        return FraudSummary(
            total_fraud_count=fraud_count,
            fraud_rate=fraud_rate,
            total_fraud_amount=total_fraud_amount,
        )