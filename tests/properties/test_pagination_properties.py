"""Property-based tests for pagination functionality."""

from datetime import datetime
from hypothesis import given, strategies as st

from transaction_api.models import Transaction
from transaction_api.pagination import PaginationService
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
    ),
    st.integers(min_value=1, max_value=10),
    st.integers(min_value=1, max_value=50),
)
def test_pagination_consistency(transactions, page, limit):
    """
    Property 3: Pagination Consistency.

    For any paginated query with page P and limit L, the returned results
    should be consistent with offset (P-1)*L and limit L, and total_count
    should equal the sum of all page sizes.

    **Validates: Requirements 2.4, 22.1, 22.3**
    """
    repo = TransactionRepository()
    repo.data_load_date = datetime.utcnow()

    # Load transactions
    for transaction in transactions:
        repo._add_transaction(transaction)

    # Get paginated results
    results, total_count = repo.get_all(page=page, limit=limit)

    # Verify total count
    assert total_count == len(transactions)

    # Verify pagination metadata
    response = PaginationService.create_paginated_response(
        results, page, limit, total_count
    )
    assert response.pagination.total_count == total_count
    assert response.pagination.page == page
    assert response.pagination.limit == limit

    # Verify total pages calculation
    expected_total_pages = (total_count + limit - 1) // limit
    assert response.pagination.total_pages == expected_total_pages

    # Verify has_next_page
    expected_has_next = page < expected_total_pages
    assert response.pagination.has_next_page == expected_has_next

    # Verify result size
    expected_size = min(limit, max(0, total_count - (page - 1) * limit))
    assert len(results) == expected_size