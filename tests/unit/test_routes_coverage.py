"""Unit tests to improve route coverage."""

import pytest
from fastapi.testclient import TestClient
from transaction_api.main import app
from transaction_api import app_context
from transaction_api.repository import TransactionRepository


@pytest.fixture(scope="module")
def client():
    """Create test client."""
    return TestClient(app)


@pytest.fixture(scope="module", autouse=True)
def setup_repository():
    """Setup repository with test data."""
    repo = TransactionRepository()
    repo.load_from_csv("./data/transactions.csv")
    app_context.repository = repo
    yield
    app_context.repository = None


class TestCustomerRoutesExtended:
    """Extended tests for customer routes."""

    def test_get_customer_details_with_transactions(self, client):
        """Test getting customer details with transactions."""
        response = client.get("/api/customers/1556")
        assert response.status_code == 200
        data = response.json()
        assert "customer_id" in data
        assert "transaction_count" in data

    def test_get_top_customers_with_limit(self, client):
        """Test getting top customers with specific limit."""
        response = client.get("/api/customers/Ranked/top?n=5")
        assert response.status_code == 200
        data = response.json()
        assert len(data) <= 5


lass TestTransactionRoutesExtended:
    """Extended tests for transaction routes."""

    def test_get_transaction_by_id_success(self, client):
        """Test getting transaction by ID."""
        response = client.get("/api/transaction?page=1&limit=1")
        assert response.status_code == 200
        data = response.json()
        if data.get("data"):
            transaction_id = data["data"][0]["id"]
            response = client.get(f"/api/transaction/{transaction_id}")
            assert response.status_code == 200

    def test_search_transactions_with_multiple_filters(self, client):
        """Test searching transactions with multiple filters."""
        response = client.post(
            "/api/transaction/transactionResearch/search",
            json={
                "min_amount": 50,
                "max_amount": 1000,
                "use_chip": "Swipe Transaction",
            },
        )
        assert response.status_code == 200

    def test_get_customer_transactions(self, client):
        """Test getting transactions for a customer."""
        response = client.get(
            "/api/transaction/by-customer/1556?page=1&limit=10"
        )
        assert response.status_code == 200

    def test_get_merchant_transactions(self, client):
        """Test getting merchant transactions."""
        response = client.get(
            "/api/transaction/to-customer/1556?page=1&limit=10"
        )
        assert response.status_code == 200


class TestFraudRoutesExtended:
    """Extended tests for fraud routes."""

    def test_predict_fraud(self, client):
        """Test fraud prediction."""
        response = client.get("/api/transaction?page=1&limit=1")
        if response.status_code == 200:
            data = response.json()
            if data.get("data"):
                transaction = data["data"][0]
                response = client.post(
                    "/api/fraud/predict",
                    json=transaction,
                )
                assert response.status_code == 200

class TestStatisticsRoutesExtended:
    """Extended tests for statistics routes."""

    def test_get_overview_stats(self, client):
        """Test getting overview statistics."""
        response = client.get("/api/stats/overview")
        assert response.status_code == 200

    def test_get_amount_distribution(self, client):
        """Test getting amount distribution."""
        response = client.get("/api/stats/amount-distribution")
        assert response.status_code == 200

    def test_get_stats_by_type(self, client):
        """Test getting statistics by type."""
        response = client.get("/api/stats/by-type")
        assert response.status_code == 200


class TestSystemRoutesExtended:
    """Extended tests for system routes."""

    def test_health_check_response(self, client):
        """Test health check response structure."""
        response = client.get("/api/system/health")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data

    def test_metadata_response(self, client):
        """Test metadata response structure."""
        response = client.get("/api/system/metadata")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)     
