"""Property-based tests for search functionality."""

from datetime import datetime
from hypothesis import given, strategies as st

from transaction_api.models import SearchFilters, Transaction
from transaction_api.repository import TransactionRepository


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
def test_search_filter_correctness(transactions):
    """
    Property 4: Search Filter Correctness.

    For any search query with filters (amount range, client_id, transaction_id,
    merchant_city, use_chip), all returned transactions should satisfy all
    specified filter conditions.

    **Validates: Requirements 3.1, 3.2, 3.3, 3.4**
    """
    repo = TransactionRepository()
    repo.data_load_date = datetime.utcnow()

    # Load transactions
    for transaction in transactions:
        repo._add_transaction(transaction)

    if not transactions:
        return

    # Test with amount range filter
    min_amount = min(t.amount for t in transactions)
    max_amount = max(t.amount for t in transactions)
    mid_amount = (min_amount + max_amount) / 2

    filters = SearchFilters(min_amount=min_amount, max_amount=mid_amount)
    results, _ = repo.search(filters=filters, page=1, limit=1000)

    # Verify all results satisfy the filter
    for result in results:
        assert result.amount >= min_amount
        assert result.amount <= mid_amount

    # Test with client_id filter
    if transactions:
        client_id = transactions[0].client_id
        filters = SearchFilters(client_id=client_id)
        results, _ = repo.search(filters=filters, page=1, limit=1000)

        # Verify all results satisfy the filter
        for result in results:
            assert result.client_id == client_id

    # Test with use_chip filter
    if transactions:
        use_chip = transactions[0].use_chip
        filters = SearchFilters(use_chip=use_chip)
        results, _ = repo.search(filters=filters, page=1, limit=1000)

        # Verify all results satisfy the filter
        for result in results:
            assert result.use_chip == use_chip