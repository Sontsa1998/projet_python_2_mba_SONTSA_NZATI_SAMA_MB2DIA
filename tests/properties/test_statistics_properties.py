"""Property-based tests for statistics functionality."""

from datetime import datetime
from hypothesis import given, strategies as st

from transaction_api.models import Transaction
from transaction_api.repository import TransactionRepository
from transaction_api.services.statistics_service import StatisticsService


def transaction_strategy():
    """Generate valid transaction objects."""
    return st.builds(
        Transaction,
        id=st.text(min_size=1, max_size=20),
        date=st.datetimes(
            min_value=datetime(2020, 1, 1), max_value=datetime(2024, 12, 31)
        ),
        client_id=st.text(min_size=1, max_size=10),
        card_id=st.text(min_size=1, max_size=20),
        amount=st.floats(min_value=0.01, max_value=10000.0),
        use_chip=st.sampled_from(
            ["Swipe Transaction", "Online Transaction", "Chip Transaction"]
        ),
        merchant_id=st.text(min_size=1, max_size=10),
        merchant_city=st.text(min_size=1, max_size=20),
        merchant_state=st.text(min_size=2, max_size=2),
        zip=st.text(min_size=5, max_size=5),
        mcc=st.text(min_size=4, max_size=4),
        errors=st.none() | st.text(min_size=1, max_size=50),
    )


@given(
    st.lists(
        transaction_strategy(),
        min_size=1,
        max_size=100,
        unique_by=lambda t: t.id,
    )
)
def test_statistics_aggregation_correctness(transactions):
    """
    Property 9: Statistics Aggregation Correctness.

    For any overview statistics query, the total_amount should equal the sum
    of all transaction amounts, and average_amount should equal total_amount
    divided by total_count.

    **Validates: Requirements 9.1, 9.2**
    """
    repo = TransactionRepository()
    repo.data_load_date = datetime.utcnow()
    service = StatisticsService(repo)

    # Load transactions
    for transaction in transactions:
        repo._add_transaction(transaction)

    # Get overview stats
    stats = service.get_overview_stats()

    # Verify total count
    assert stats.total_count == len(transactions)

    # Verify total amount
    expected_total = sum(t.amount for t in transactions)
    assert abs(stats.total_amount - expected_total) < 0.01

    # Verify average amount
    expected_average = (
        expected_total / len(transactions) if transactions else 0.0
    )
    assert abs(stats.average_amount - expected_average) < 0.01


@given(
    st.lists(
        transaction_strategy(),
        min_size=1,
        max_size=100,
        unique_by=lambda t: t.id,
    )
)
def test_amount_distribution_completeness(transactions):
    """
    Property 10: Amount Distribution Completeness.

    For any amount distribution query, the sum of all bucket counts should
    equal the total transaction count, and all transactions should fall into
    exactly one bucket.

    **Validates: Requirements 10.1, 10.2, 10.3**
    """
    repo = TransactionRepository()
    repo.data_load_date = datetime.utcnow()
    service = StatisticsService(repo)

    # Load transactions
    for transaction in transactions:
        repo._add_transaction(transaction)

    # Get amount distribution
    distribution = service.get_amount_distribution()

    # Verify sum of counts equals total
    total_count = sum(b.count for b in distribution.buckets)
    assert total_count == len(transactions)

    # Verify percentages sum to 100 (approximately)
    total_percentage = sum(b.percentage for b in distribution.buckets)
    assert abs(total_percentage - 100.0) < 0.1 or len(transactions) == 0


@given(
    st.lists(
        transaction_strategy(),
        min_size=1,
        max_size=100,
        unique_by=lambda t: t.id,
    )
)
def test_type_statistics_accuracy(transactions):
    """
    Property 11: Type Statistics Accuracy.

    For any statistics by type query, for each type, the count should equal
    the number of transactions with that type, and the sum of all counts
    should equal total transaction count.

    **Validates: Requirements 11.1, 11.2, 11.3**
    """
    repo = TransactionRepository()
    repo.data_load_date = datetime.utcnow()
    service = StatisticsService(repo)

    # Load transactions
    for transaction in transactions:
        repo._add_transaction(transaction)

    # Get type statistics
    type_stats = service.get_stats_by_type()

    # Verify sum of counts equals total
    total_count = sum(t.count for t in type_stats)
    assert total_count == len(transactions)

    # Verify each type count is correct
    for type_stat in type_stats:
        expected_count = len(repo.get_all_by_type(type_stat.type))
        assert type_stat.count == expected_count

    # Verify sorted by count descending
    counts = [t.count for t in type_stats]
    assert counts == sorted(counts, reverse=True)


@given(
    st.lists(
        transaction_strategy(),
        min_size=1,
        max_size=100,
        unique_by=lambda t: t.id,
    )
)
def test_daily_statistics_aggregation(transactions):
    """
    Property 12: Daily Statistics Aggregation.

    For any daily statistics query, for each day, the count should equal the
    number of transactions on that day, and the sum of all daily counts should
    equal total transaction count.

    **Validates: Requirements 12.1, 12.2, 12.3**
    """
    repo = TransactionRepository()
    repo.data_load_date = datetime.utcnow()
    service = StatisticsService(repo)

    # Load transactions
    for transaction in transactions:
        repo._add_transaction(transaction)

    if not transactions:
        return

    # Get daily statistics
    daily_stats = service.get_daily_stats()

    # Verify sum of counts equals total
    total_count = sum(d["count"] for d in daily_stats)
    assert total_count == len(transactions)

    # Verify each day's count is correct
    for day_stat in daily_stats:
        expected_count = len(
            [
                t
                for t in transactions
                if t.date.date()
                == datetime.fromisoformat(day_stat["date"]).date()
            ]
        )
        assert day_stat["count"] == expected_count