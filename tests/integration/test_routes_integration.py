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


