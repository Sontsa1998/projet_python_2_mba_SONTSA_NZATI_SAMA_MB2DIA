"""Property-based tests for customer functionality."""

from datetime import datetime
from hypothesis import given, strategies as st

from transaction_api.models import Transaction
from transaction_api.repository import TransactionRepository
from transaction_api.services.customer_service import CustomerService


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
def test_customer_list_completeness(transactions):
    """
    Property 16: Customer List Completeness.

    For any customer list query, all unique customer_ids from transactions
    should appear in the results (across all pages).
    Each customer should have transaction_count equal to the number of
    transactions for that customer.

    **Validates: Requirements 16.1, 16.2, 16.3**
    """
    repo = TransactionRepository()
    repo.data_load_date = datetime.utcnow()
    service = CustomerService(repo)

    # Load transactions
    for transaction in transactions:
        repo._add_transaction(transaction)

    # Get all customers
    response = service.get_all_customers(page=1, limit=1000)

    # Verify all unique customer IDs are present
    unique_customer_ids = set(t.client_id for t in transactions)
    returned_customer_ids = set(c.customer_id for c in response.data)
    assert unique_customer_ids == returned_customer_ids

    # Verify each customer's transaction count
    for customer in response.data:
        expected_count = len(
            [t for t in transactions if t.client_id == customer.customer_id]
        )
        assert customer.transaction_count == expected_count


@given(
    st.lists(
        transaction_strategy(),
        min_size=1,
        max_size=100,
        unique_by=lambda t: t.id,
    )
)
def test_customer_details_accuracy(transactions):
    """
    Property 17: Customer Details Accuracy.

    For any customer_id, the returned customer details should have
    transaction_count equal to the number of transactions for that customer,
    and average_amount should equal total_amount divided by transaction_count.

    **Validates: Requirements 17.1, 17.2**
    """
    repo = TransactionRepository()
    repo.data_load_date = datetime.utcnow()
    service = CustomerService(repo)

    # Load transactions
    for transaction in transactions:
        repo._add_transaction(transaction)

    # Get all unique customer IDs
    unique_customer_ids = set(t.client_id for t in transactions)

    # For each customer, verify details accuracy
    for customer_id in unique_customer_ids:
        customer = service.get_customer_details(customer_id)

        # Verify transaction count
        expected_count = len(
            [t for t in transactions if t.client_id == customer_id]
        )
        assert customer.transaction_count == expected_count

        # Verify total amount
        expected_total = sum(
            t.amount for t in transactions if t.client_id == customer_id
        )
        assert abs(customer.total_amount - expected_total) < 0.01

        # Verify average amount
        expected_average = (
            expected_total / expected_count if expected_count > 0 else 0.0
        )
        assert abs(customer.average_amount - expected_average) < 0.01


@given(
    st.lists(
        transaction_strategy(),
        min_size=1,
        max_size=100,
        unique_by=lambda t: t.id,
    )
)
def test_top_customers_ranking(transactions):
    """
    Property 18: Top Customers Ranking.

    For any top customers query with n, the returned customers should
    be sorted by transaction_count in descending order, and the number of
    returned customers should be at most n.

    **Validates: Requirements 18.1, 18.2, 18.3**
    """
    repo = TransactionRepository()
    repo.data_load_date = datetime.utcnow()
    service = CustomerService(repo)

    # Load transactions
    for transaction in transactions:
        repo._add_transaction(transaction)

    # Get top customers
    n = 10
    top_customers = service.get_top_customers(n=n)

    # Verify number of returned customers
    unique_customer_count = len(set(t.client_id for t in transactions))
    expected_count = min(n, unique_customer_count)
    assert len(top_customers) == expected_count

    # Verify sorted by transaction count descending
    counts = [c.transaction_count for c in top_customers]
    assert counts == sorted(counts, reverse=True)