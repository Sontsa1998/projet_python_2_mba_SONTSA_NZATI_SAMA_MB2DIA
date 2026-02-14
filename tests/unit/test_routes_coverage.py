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


