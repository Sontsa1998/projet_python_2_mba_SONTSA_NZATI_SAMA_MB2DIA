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
    
    def get_amount_distribution(self) -> AmountDistribution:
        """Get amount distribution statistics."""
        transactions = self.repository.get_all_transactions()
        total_count = len(transactions)

        if total_count == 0:
            buckets = [
                AmountBucket(range=b["label"], count=0, percentage=0.0)
                for b in AMOUNT_BUCKETS
            ]
            return AmountDistribution(buckets=buckets)

        # Count transactions in each bucket
        bucket_counts: dict = defaultdict(int)
        for transaction in transactions:
            for bucket in AMOUNT_BUCKETS:
                if bucket["min"] <= transaction.amount < bucket["max"]:
                    bucket_counts[bucket["label"]] += 1
                    break

        # Create bucket responses
        buckets = []
        for bucket in AMOUNT_BUCKETS:
            count = bucket_counts[bucket["label"]]
            if total_count > 0:
                percentage = count / total_count * 100
            else:
                percentage = 0.0
            buckets.append(
                AmountBucket(
                    range=bucket["label"],
                    count=count,
                    percentage=percentage,
                )
            )

        return AmountDistribution(buckets=buckets)

    def get_stats_by_type(self) -> List[TypeStats]:
        """Get statistics grouped by transaction type."""
        types = self.repository.get_all_types()
        type_stats = []

        for mcc in types:
            transactions = self.repository.get_all_by_type(mcc)
            if transactions:
                count = len(transactions)
                total_amount = sum(t.amount for t in transactions)
                average_amount = total_amount / count if count > 0 else 0.0

                type_stats.append(
                    TypeStats(
                        type=mcc,
                        count=count,
                        total_amount=total_amount,
                        average_amount=average_amount,
                    )
                )

        # Sort by count descending
        type_stats.sort(key=lambda x: x.count, reverse=True)
        return type_stats
    
    def get_daily_stats(self) -> list[dict]:
        """Get daily statistics grouped by date."""
        transactions = self.repository.get_all_transactions()

        # Group by date
        daily_data = defaultdict(list)
        for transaction in transactions:
            day = transaction.date.date()
            daily_data[day].append(transaction)

        # Create daily stats
        daily_stats = []
        for day in sorted(daily_data.keys()):
            transactions_on_day = daily_data[day]
            count = len(transactions_on_day)
            total_amount = sum(t.amount for t in transactions_on_day)
            average_amount = total_amount / count if count > 0 else 0.0

            daily_stats.append(
                {
                    "date": str(day),
                    "count": count,
                    "total_amount": total_amount,
                    "average_amount": average_amount,
                }
            )

        return daily_stats
