"""Property-based tests for transaction types and recent transactions."""

from datetime import datetime
from hypothesis import given, strategies as st

from transaction_api.models import Transaction
from transaction_api.repository import TransactionRepository
from transaction_api.services.transaction_service import TransactionService


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
def test_transaction_type_uniqueness(transactions):
    """
    Property 5: Transaction Type Uniqueness.

    For any transaction type returned from /api/transactions/types, the count
    should equal the number of transactions with that type, and the sum of all
    counts should equal total transaction count.

    **Validates: Requirements 4.1, 4.2, 4.3**
    """
    repo = TransactionRepository()
    repo.data_load_date = datetime.utcnow()
    service = TransactionService(repo)

    # Load transactions
    for transaction in transactions:
        repo._add_transaction(transaction)

    # Get transaction types (now based on use_chip)
    types = service.get_transaction_types()

    # Verify sum of counts equals total
    total_count = sum(t["count"] for t in types)
    assert total_count == len(transactions)

    # Verify each type count is correct
    for type_info in types:
        use_chip = type_info["type"]
        expected_count = len(repo.get_all_by_use_chip(use_chip))
        assert type_info["count"] == expected_count

    # Verify sorted by count descending
    counts = [t["count"] for t in types]
    assert counts == sorted(counts, reverse=True)


@given(
    st.lists(
        transaction_strategy(),
        min_size=1,
        max_size=100,
        unique_by=lambda t: t.id,
    )
)
def test_recent_transactions_ordering(transactions):
    """
    Property 6: Recent Transactions Ordering.

    For any recent transactions query, returned transactions should be sorted
    by date in descending order, with the first transaction having the most
    recent date.

    **Validates: Requirements 5.1, 5.2**
    """
    repo = TransactionRepository()
    repo.data_load_date = datetime.utcnow()
    service = TransactionService(repo)

    # Load transactions
    for transaction in transactions:
        repo._add_transaction(transaction)

    # Get recent transactions
    response = service.get_recent_transactions(limit=100)

    # Verify sorted by date descending
    dates = [t.date for t in response.data]
    assert dates == sorted(dates, reverse=True)

    # Verify first transaction is most recent
    if response.data:
        assert response.data[0].date == max(t.date for t in transactions)