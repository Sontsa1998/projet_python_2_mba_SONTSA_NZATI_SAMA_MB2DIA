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

