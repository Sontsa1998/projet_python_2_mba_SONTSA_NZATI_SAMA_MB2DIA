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


@given(
    st.lists(
        transaction_strategy(),
        min_size=1,
        max_size=100,
        unique_by=lambda t: t.id,
    )
)
def test_fraud_type_statistics_accuracy(transactions):
    """
    Property 14: Fraud Type Statistics Accuracy.

    For any fraud by use_chip query, for each use_chip type, the fraud
    count should equal the number of fraudulent transactions with that type,
    and fraud_rate should be fraud_count divided by total transactions of
    that type.

    **Validates: Requirements 14.1, 14.2, 14.3**
    """
    repo = TransactionRepository()
    repo.data_load_date = datetime.utcnow()
    service = FraudService(repo)

    # Load transactions
    for transaction in transactions:
        repo._add_transaction(transaction)

    # Get fraud by use_chip type
    fraud_stats = service.get_fraud_by_type()

    # Verify each use_chip type's fraud count and rate
    for type_stat in fraud_stats:
        use_chip_transactions = repo.get_all_by_use_chip(type_stat.type)
        expected_fraud_count = len(
            [t for t in use_chip_transactions if t.errors]
        )
        expected_total_count = len(use_chip_transactions)
        expected_fraud_rate = (
            expected_fraud_count / expected_total_count
            if expected_total_count > 0
            else 0.0
        )

        assert type_stat.fraud_count == expected_fraud_count
        assert type_stat.total_count == expected_total_count
        assert abs(type_stat.fraud_rate - expected_fraud_rate) < 0.001

    # Verify sorted by fraud rate descending
    fraud_rates = [t.fraud_rate for t in fraud_stats]
    assert fraud_rates == sorted(fraud_rates, reverse=True)


@given(transaction_strategy())
def test_fraud_prediction_score_range(transaction):
    """
    Property 15: Fraud Prediction Score Range.

    For any fraud prediction query, the returned fraud_score should be between
    0.0 and 1.0 (inclusive), and the reasoning field should be non-empty.

    **Validates: Requirements 15.1, 15.2, 15.3**
    """
    repo = TransactionRepository()
    repo.data_load_date = datetime.utcnow()
    service = FraudService(repo)

    # Predict fraud
    prediction = service.predict_fraud(transaction)

    # Verify score is in range
    assert 0.0 <= prediction.fraud_score <= 1.0

    # Verify reasoning is non-empty
    assert len(prediction.reasoning) > 0