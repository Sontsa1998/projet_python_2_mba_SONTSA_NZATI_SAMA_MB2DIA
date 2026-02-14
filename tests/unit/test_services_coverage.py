"""Unit tests to improve service coverage."""

import pytest
from transaction_api.repository import TransactionRepository
from transaction_api.services.customer_service import CustomerService
from transaction_api.services.fraud_service import FraudService
from transaction_api.services.statistics_service import StatisticsService
from transaction_api.services.health_service import HealthService
from transaction_api.services.transaction_service import TransactionService

@pytest.fixture(scope="module")
def repository():
    """Create repository with test data."""
    repo = TransactionRepository()
    repo.load_from_csv("./data/transactions.csv")
    return repo


class TestCustomerServiceExtended:
    """Extended tests for customer service."""

    def test_get_all_customers_pagination(self, repository):
        """Test getting all customers with pagination."""
        service = CustomerService(repository)
        result = service.get_all_customers(page=1, limit=10)
        assert hasattr(result, "data")
        assert hasattr(result, "pagination")
        assert result.pagination.page == 1
    def test_get_customer_details_nonexistent(self, repository):
        """Test getting nonexistent customer."""
        service = CustomerService(repository)
        result = service.get_customer_details("nonexistent_id")
        assert result.customer_id == "nonexistent_id"
        assert result.transaction_count == 0

    def test_get_top_customers_limit(self, repository):
        """Test getting top customers with limit."""
        service = CustomerService(repository)
        result = service.get_top_customers(n=5)
        assert len(result) <= 5
