"""Unit tests for TransactionService."""

import pytest

from transaction_api.exceptions import TransactionNotFound
from transaction_api.services.transaction_service import TransactionService


@pytest.fixture
def service(repository_with_data):
    """Create a transaction service with sample data."""
    return TransactionService(repository_with_data)


def test_get_transaction_by_id_existing(service, sample_transactions):
    """Test getting an existing transaction by ID."""
    transaction = service.get_transaction_by_id("1")
    assert transaction.id == "1"
    assert transaction.client_id == "C001"
    assert transaction.amount == 100.0


def test_get_transaction_by_id_not_found(service):
    """Test getting a non-existent transaction."""
    with pytest.raises(TransactionNotFound):
        service.get_transaction_by_id("nonexistent")


def test_delete_transaction_existing(service):
    """Test deleting an existing transaction."""
    service.delete_transaction("1")
    with pytest.raises(TransactionNotFound):
        service.get_transaction_by_id("1")


def test_delete_transaction_not_found(service):
    """Test deleting a non-existent transaction."""
    with pytest.raises(TransactionNotFound):
        service.delete_transaction("nonexistent")


def test_get_all_transactions(service):
    """Test getting all transactions with pagination."""
    response = service.get_all_transactions(page=1, limit=10)
    assert response.pagination.page == 1
    assert response.pagination.limit == 10
    assert response.pagination.total_count == 3
    assert len(response.data) == 3


def test_get_transaction_types(service):
    """Test getting transaction types."""
    types = service.get_transaction_types()
    assert len(types) > 0
    assert all("type" in t and "count" in t for t in types)
    # Verify sorted by count descending
    counts = [t["count"] for t in types]
    assert counts == sorted(counts, reverse=True)


def test_get_recent_transactions(service):
    """Test getting recent transactions."""
    response = service.get_recent_transactions(limit=10)
    assert response.pagination.limit == 10
    assert len(response.data) > 0
    # Verify sorted by date descending
    dates = [t.date for t in response.data]
    assert dates == sorted(dates, reverse=True)


def test_get_customer_transactions(service):
    """Test getting transactions for a customer."""
    response = service.get_customer_transactions(
        customer_id="C001", page=1, limit=10
    )
    assert response.pagination.total_count == 2
    assert all(t.client_id == "C001" for t in response.data)


def test_get_merchant_transactions(service):
    """Test getting transactions for a merchant."""
    response = service.get_merchant_transactions(
        merchant_id="M001", page=1, limit=10
    )
    assert response.pagination.total_count == 2
    assert all(t.merchant_id == "M001" for t in response.data)
