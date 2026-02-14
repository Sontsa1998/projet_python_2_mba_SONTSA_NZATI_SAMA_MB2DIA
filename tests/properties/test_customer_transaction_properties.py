"""Property-based tests for customer transaction functionality."""

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
def test_customer_transaction_filtering(transactions):
    """
    Property 8: Customer Transaction Filtering.

    For any customer_id, all transactions returned from
    /api/transactions/by-customer/{customer_id} should have client_id equal
    to that customer_id.

    **Validates: Requirements 7.1**
    """
    repo = TransactionRepository()
    repo.data_load_date = datetime.utcnow()
    service = TransactionService(repo)

    # Load transactions
    for transaction in transactions:
        repo._add_transaction(transaction)

    # Get all unique customer IDs
    customer_ids = set(t.client_id for t in transactions)

    # For each customer, verify returned transactions have
    # a matching client_id
    for customer_id in customer_ids:
        response = service.get_customer_transactions(
            customer_id=customer_id, page=1, limit=1000
        )

        # Verify all results have matching client_id
        for transaction in response.data:
            assert transaction.client_id == customer_id
