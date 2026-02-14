"""Property-based tests for error handling and performance."""

from datetime import datetime
from hypothesis import given, strategies as st

from transaction_api.exceptions import InvalidPaginationParameters
from transaction_api.models import Transaction
from transaction_api.pagination import PaginationService
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
    st.integers(min_value=-10, max_value=0),
    st.integers(min_value=-10, max_value=0),
)
def test_invalid_pagination_handling(page, limit):
    """
    Property 22: Invalid Pagination Handling.

    For any pagination request with invalid parameters
    (negative page, limit > 1000, etc.), the API should return a 400
    error with descriptive validation details.

    **Validates: Requirements 2.5**
    """
    # Test invalid page
    if page < 1:
        try:
            PaginationService.validate_pagination_params(page, 50)
            assert False, "Should have raised InvalidPaginationParameters"
        except InvalidPaginationParameters:
            pass

    # Test invalid limit
    if limit < 1:
        try:
            PaginationService.validate_pagination_params(1, limit)
            assert False, "Should have raised InvalidPaginationParameters"
        except InvalidPaginationParameters:
            pass


@given(
    st.lists(
        transaction_strategy(),
        min_size=1,
        max_size=100,
        unique_by=lambda t: t.id,
    )
)
def test_non_existent_resource_handling(transactions):
    """
    Property 23: Non-existent Resource Handling.

    For any query for a non-existent transaction ID or customer_id, the API
    should return a 404 error with a descriptive message.

    **Validates: Requirements 2.3, 17.3**
    """
    repo = TransactionRepository()
    repo.data_load_date = datetime.utcnow()
    service = TransactionService(repo)

    # Load transactions
    for transaction in transactions:
        repo._add_transaction(transaction)

    # Test non-existent transaction
    from transaction_api.exceptions import TransactionNotFound

    try:
        service.get_transaction_by_id("nonexistent_id_12345")
        assert False, "Should have raised TransactionNotFound"
    except TransactionNotFound:
        pass