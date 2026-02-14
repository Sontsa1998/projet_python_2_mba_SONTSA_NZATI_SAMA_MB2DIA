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

class TestFraudServiceExtended:
    """Extended tests for fraud service."""

    def test_get_fraud_summary(self, repository):
        """Test getting fraud summary."""
        service = FraudService(repository)
        result = service.get_fraud_summary()
        assert hasattr(result, "total_fraud_count")
        assert hasattr(result, "fraud_rate")

    def test_get_fraud_by_type(self, repository):
        """Test getting fraud by type."""
        service = FraudService(repository)
        result = service.get_fraud_by_type()
        assert isinstance(result, list)
        if result:
            assert hasattr(result[0], "type")
            assert hasattr(result[0], "fraud_count")

    def test_predict_fraud(self, repository):
        """Test fraud prediction."""
        service = FraudService(repository)
        transactions = repository.get_all_transactions()
        if transactions:
            result = service.predict_fraud(transactions[0])
            assert hasattr(result, "fraud_score")
            assert hasattr(result, "reasoning")


class TestStatisticsServiceExtended:
    """Extended tests for statistics service."""

    def test_get_overview_stats(self, repository):
        """Test getting overview statistics."""
        service = StatisticsService(repository)
        result = service.get_overview_stats()
        assert hasattr(result, "total_count")
        assert hasattr(result, "total_amount")

    def test_get_amount_distribution(self, repository):
        """Test getting amount distribution."""
        service = StatisticsService(repository)
        result = service.get_amount_distribution()
        assert hasattr(result, "buckets")
        assert isinstance(result.buckets, list)

    def test_get_stats_by_type(self, repository):
        """Test getting statistics by type."""
        service = StatisticsService(repository)
        result = service.get_stats_by_type()
        assert isinstance(result, list)

    def test_get_daily_stats(self, repository):
        """Test getting daily statistics."""
        service = StatisticsService(repository)
        result = service.get_daily_stats()
        assert isinstance(result, list)

