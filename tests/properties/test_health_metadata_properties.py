"""Property-based tests for health and metadata functionality."""

from datetime import datetime
from hypothesis import given, strategies as st

from transaction_api.models import Transaction
from transaction_api.repository import TransactionRepository
from transaction_api.services.health_service import HealthService


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
        min_size=0,
        max_size=100,
        unique_by=lambda t: t.id,
    )
)
def test_health_check_consistency(transactions):
    """
    Property 19: Health Check Consistency.

    For any health check query, if the system is healthy, the response should
    include a valid status and response_time_ms should be a positive number.

    **Validates: Requirements 19.1, 19.2, 19.3**
    """
    repo = TransactionRepository()
    repo.data_load_date = datetime.utcnow()
    service = HealthService(repo)

    # Load transactions
    for transaction in transactions:
        repo._add_transaction(transaction)

    # Check health
    health = service.check_health()

    # Verify status is valid
    assert health.status in ("healthy", "unhealthy")

    # Verify response time is positive
    assert health.response_time_ms >= 0


@given(
    st.lists(
        transaction_strategy(),
        min_size=1,
        max_size=100,
        unique_by=lambda t: t.id,
    )
)
def test_metadata_accuracy(transactions):
    """
    Property 20: Metadata Accuracy.

    For any metadata query, the total_transaction_count should equal the actual
    number of transactions in the system, and min_date should be less than or
    equal to max_date.

    **Validates: Requirements 20.1, 20.2, 20.3**
    """
    repo = TransactionRepository()
    repo.data_load_date = datetime.utcnow()
    service = HealthService(repo)

    # Load transactions
    for transaction in transactions:
        repo._add_transaction(transaction)

    # Get metadata
    metadata = service.get_metadata()

    # Verify total count
    assert metadata.total_transaction_count == len(transactions)

    # Verify date range
    assert metadata.min_date <= metadata.max_date

    # Verify API version is set
    assert len(metadata.api_version) > 0