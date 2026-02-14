"""Statistics service for business logic."""

from collections import defaultdict
from datetime import datetime
from typing import List

from transaction_api.config import AMOUNT_BUCKETS
from transaction_api.logging_config import get_logger
from transaction_api.models import (
    AmountBucket,
    AmountDistribution,
    OverviewStats,
    TypeStats,
)
from transaction_api.repository import TransactionRepository

logger = get_logger(__name__)


class StatisticsService:
    """Service for statistics operations."""

    def __init__(self, repository: TransactionRepository) -> None:
        """Initialize the service."""
        self.repository = repository