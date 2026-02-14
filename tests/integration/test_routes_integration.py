"""Integration tests for all API routes."""

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


class TestCustomerRoutes:
    """Test customer routes."""

    def test_get_all_customers(self, client):
        """Test getting all customers with pagination."""
        response = client.get("/api/customers?page=1&limit=10")
        assert response.status_code == 200
        data = response.json()
        assert "data" in data or isinstance(data, list)

    def test_get_all_customers_invalid_pagination(self, client):
        """Test getting customers with invalid pagination."""
        response = client.get("/api/customers?page=0&limit=0")
        # Should either return 200 with corrected pagination,
        # 400, or 422 for validation error
        assert response.status_code in [200, 400, 422]

    def test_get_customer_details(self, client):
        """Test getting customer details."""
        response = client.get("/api/customers/1556")
        assert response.status_code == 200
        data = response.json()
        assert data["customer_id"] == "1556"
        assert "transaction_count" in data
        assert "total_amount" in data
        assert "average_amount" in data

    def test_get_customer_details_nonexistent(self, client):
        """Test getting nonexistent customer."""
        response = client.get("/api/customers/nonexistent")
        assert response.status_code == 200
        data = response.json()
        assert data["customer_id"] == "nonexistent"
        assert data["transaction_count"] == 0

    def test_get_top_customers(self, client):
        """Test getting top customers."""
        response = client.get("/api/customers/Ranked/top?n=10")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) <= 10
        if len(data) > 1:
            assert data[0]["transaction_count"] >= data[1]["transaction_count"]

    def test_get_top_customers_default(self, client):
        """Test getting top customers with default n."""
        response = client.get("/api/customers/Ranked/top")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) <= 50


class TestTransactionRoutes:
    """Test transaction routes."""

    def test_get_all_transactions(self, client):
        """Test getting all transactions."""
        response = client.get("/api/transaction?page=1&limit=10")
        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        assert len(data["data"]) <= 10

    def test_get_transaction_by_id(self, client):
        """Test getting transaction by ID."""
        response = client.get("/api/transaction?page=1&limit=1")
        assert response.status_code == 200
        data = response.json()
        if data["data"]:
            transaction_id = data["data"][0]["id"]
            response = client.get(f"/api/transaction/{transaction_id}")
            assert response.status_code == 200
            assert response.json()["id"] == transaction_id

    def test_search_transactions(self, client):
        """Test searching transactions."""
        response = client.post(
            "/api/transaction/transactionResearch/search",
            json={"client_id": "1556"},
        )
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, (dict, list))

    def test_search_transactions_by_amount(self, client):
        """Test searching transactions by amount range."""
        response = client.post(
            "/api/transaction/transactionResearch/search",
            json={
                "min_amount": 100,
                "max_amount": 500,
                "page": 1,
                "limit": 10,
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        for transaction in data["data"]:
            assert 100 <= transaction["amount"] <= 500

    def test_search_transactions_by_use_chip(self, client):
        """Test searching transactions by use_chip."""
        response = client.post(
            "/api/transaction/transactionResearch/search",
            json={"use_chip": "Swipe Transaction", "page": 1, "limit": 10},
        )
        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        for transaction in data["data"]:
            assert transaction["use_chip"] == "Swipe Transaction"

    def test_search_transactions_by_merchant_city(self, client):
        """Test searching transactions by merchant city."""
        response = client.post(
            "/api/transaction/transactionResearch/search",
            json={"merchant_city": "Beulah", "page": 1, "limit": 10},
        )
        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        for transaction in data["data"]:
            assert transaction["merchant_city"] == "Beulah"

    def test_get_recent_transactions(self, client):
        """Test getting recent transactions."""
        response = client.get("/api/transaction/Latest/recent?limit=10")
        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        assert len(data["data"]) <= 10

    def test_get_transaction_types(self, client):
        """Test getting transaction types."""
        response = client.get("/api/transaction/Type/types")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0


class TestFraudRoutes:
    """Test fraud routes."""

    def test_get_fraud_transactions(self, client):
        """Test getting fraud transactions."""
        response = client.get("/api/fraud/summary")
        assert response.status_code == 200
        data = response.json()
        assert "total_fraud_count" in data or "fraud_rate" in data

    def test_get_fraud_by_type(self, client):
        """Test getting fraud statistics by use_chip type."""
        response = client.get("/api/fraud/by-type")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        for item in data:
            assert "type" in item
            assert "fraud_count" in item
            assert "fraud_rate" in item
            assert "total_count" in item


