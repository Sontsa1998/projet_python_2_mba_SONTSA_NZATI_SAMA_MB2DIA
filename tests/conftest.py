"""Pytest configuration and fixtures."""

import pytest
from datetime import datetime
from transaction_api.models import Transaction
from transaction_api.repository import TransactionRepository


@pytest.fixture
def sample_transactions() -> list[Transaction]:
    """Create sample transactions for testing."""
    return [
        Transaction(
            id="1",
            date=datetime(2023, 1, 1, 12, 0, 0),
            client_id="C001",
            card_id="CARD001",
            amount=100.0,
            use_chip="Chip Transaction",
            merchant_id="M001",
            merchant_city="New York",
            merchant_state="NY",
            zip="10001",
            mcc="5411",
            errors=None,
        ),
        Transaction(
            id="2",
            date=datetime(2023, 1, 2, 12, 0, 0),
            client_id="C001",
            card_id="CARD001",
            amount=200.0,
            use_chip="Chip Transaction",
            merchant_id="M002",
            merchant_city="Boston",
            merchant_state="MA",
            zip="02101",
            mcc="5411",
            errors=None,
        ),
        Transaction(
            id="3",
            date=datetime(2023, 1, 3, 12, 0, 0),
            client_id="C002",
            card_id="CARD002",
            amount=150.0,
            use_chip="Swipe Transaction",
            merchant_id="M001",
            merchant_city="New York",
            merchant_state="NY",
            zip="10001",
            mcc="5812",
            errors="Fraud",
        ),
    ]


@pytest.fixture
def repository_with_data(
    sample_transactions: list[Transaction],
) -> TransactionRepository:
    """Create a repository with sample data."""
    repo = TransactionRepository()
    repo.data_load_date = datetime.utcnow()
    for transaction in sample_transactions:
        repo._add_transaction(transaction)
    return repo
