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


