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
    
    def get_overview_stats(self) -> OverviewStats:
        """Get overview statistics."""
        transactions = self.repository.get_all_transactions()

        if not transactions:
            now = datetime.utcnow()
            return OverviewStats(
                total_count=0,
                total_amount=0.0,
                average_amount=0.0,
                min_date=now,
                max_date=now,
            )

        total_count = len(transactions)
        total_amount = sum(t.amount for t in transactions)
        average_amount = total_amount / total_count if total_count > 0 else 0.0
        min_date = min(t.date for t in transactions)
        max_date = max(t.date for t in transactions)

        return OverviewStats(
            total_count=total_count,
            total_amount=total_amount,
            average_amount=average_amount,
            min_date=min_date,
            max_date=max_date,
        )