"""Property-based tests for fraud detection functionality."""

from datetime import datetime
from hypothesis import given, strategies as st

from transaction_api.models import Transaction
from transaction_api.repository import TransactionRepository
from transaction_api.services.fraud_service import FraudService


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
def test_fraud_identification_correctness(transactions):
    """
    Property 13: Fraud Identification Correctness.

    For any fraud summary query, the total_fraud_count should equal the number
    of transactions with non-null errors field, and fraud_rate should equal
    fraud_count divided by total_count.

    **Validates: Requirements 13.1, 13.2, 13.3**
    """
    repo = TransactionRepository()
    repo.data_load_date = datetime.utcnow()
    service = FraudService(repo)

    # Load transactions
    for transaction in transactions:
        repo._add_transaction(transaction)

    # Get fraud summary
    summary = service.get_fraud_summary()

    # Verify fraud count
    expected_fraud_count = len([t for t in transactions if t.errors])
    assert summary.total_fraud_count == expected_fraud_count

    # Verify fraud rate
    expected_fraud_rate = (
        expected_fraud_count / len(transactions) if transactions else 0.0
    )
    assert abs(summary.fraud_rate - expected_fraud_rate) < 0.001

    # Verify fraud amount
    expected_fraud_amount = sum(t.amount for t in transactions if t.errors)
    assert abs(summary.total_fraud_amount - expected_fraud_amount) < 0.01
