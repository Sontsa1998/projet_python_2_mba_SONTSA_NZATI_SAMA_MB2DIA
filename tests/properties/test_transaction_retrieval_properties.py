"""Property-based tests for transaction retrieval."""

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
def test_transaction_retrieval_accuracy(transactions):
    """
    Property 2: Transaction Retrieval Accuracy.

    For any transaction ID that exists in the system, querying by that ID
    should return the exact transaction that was loaded.

    **Validates: Requirements 2.2**
    """
    repo = TransactionRepository()
    repo.data_load_date = datetime.utcnow()
    service = TransactionService(repo)

    # Load transactions
    for transaction in transactions:
        repo._add_transaction(transaction)

    # Verify retrieval accuracy
    for transaction in transactions:
        retrieved = service.get_transaction_by_id(transaction.id)
        assert retrieved == transaction
        assert retrieved.id == transaction.id
        assert retrieved.date == transaction.date
        assert retrieved.amount == transaction.amount
