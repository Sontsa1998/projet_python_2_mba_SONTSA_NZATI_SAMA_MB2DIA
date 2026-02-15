"""Unit tests to improve repository coverage."""

import pytest
from transaction_api.repository import TransactionRepository

@pytest.fixture(scope="module")
def repository():
    """Create repository with test data."""
    repo = TransactionRepository()
    repo.load_from_csv("./data/transactions.csv")
    return repo


class TestRepositoryExtended:
    """Extended tests for repository."""

    def test_get_all_transactions(self, repository):
        """Test getting all transactions."""
        transactions = repository.get_all_transactions()
        assert len(transactions) > 0

    def test_get_by_id(self, repository):
        """Test getting transaction by ID."""
        transactions = repository.get_all_transactions()
        if transactions:
            transaction_id = transactions[0].id
            result = repository.get_by_id(transaction_id)
            assert result is not None
            assert result.id == transaction_id

    def test_get_by_customer(self, repository):
        """Test getting transactions by customer."""
        result, total = repository.get_by_customer("1556")
        assert isinstance(result, list)
        assert isinstance(total, int)

    def test_get_by_merchant(self, repository):
        """Test getting transactions by merchant."""
        result, total = repository.get_by_merchant("1556")
        assert isinstance(result, list)
        assert isinstance(total, int)

    def test_search(self, repository):
        """Test searching transactions."""
        from transaction_api.models import SearchFilters

        filters = SearchFilters(min_amount=100, max_amount=500)
        result, total = repository.search(filters)
        assert isinstance(result, list)
        assert isinstance(total, int)

    def test_search_by_use_chip(self, repository):
        """Test searching by use_chip."""
        from transaction_api.models import SearchFilters

        filters = SearchFilters(use_chip="Swipe Transaction")
        result, total = repository.search(filters)
        assert isinstance(result, list)

    def test_search_by_merchant_city(self, repository):
        """Test searching by merchant city."""
        from transaction_api.models import SearchFilters

        filters = SearchFilters(merchant_city="Beulah")
        result, total = repository.search(filters)
        assert isinstance(result, list)

    def test_get_fraud_transactions(self, repository):
        """Test getting fraud transactions."""
        result = repository.get_fraud_transactions()
        assert isinstance(result, list)

    def test_get_all_customers(self, repository):
        """Test getting all customers."""
        result = repository.get_all_customers()
        assert isinstance(result, list)
        assert len(result) > 0

    def test_get_all_types(self, repository):
        """Test getting all transaction types."""
        result = repository.get_all_types()
        assert isinstance(result, list)

    def test_get_all_use_chip_types(self, repository):
        """Test getting all use_chip types."""
        result = repository.get_all_use_chip_types()
        assert isinstance(result, list)

    def test_get_all_by_use_chip(self, repository):
        """Test getting transactions by use_chip."""
        use_chip_types = repository.get_all_use_chip_types()
        if use_chip_types:
            result = repository.get_all_by_use_chip(use_chip_types[0])
            assert isinstance(result, list)

    def test_get_all_by_type(self, repository):
        """Test getting transactions by type."""
        types = repository.get_all_types()
        if types:
            result = repository.get_all_by_type(types[0])
            assert isinstance(result, list)

    def test_get_all_paginated(self, repository):
        """Test getting all transactions paginated."""
        result, total = repository.get_all(page=1, limit=10)
        assert isinstance(result, list)
        assert len(result) <= 10
        assert isinstance(total, int)

    def test_delete_transaction(self, repository):
        """Test deleting a transaction."""
        transactions = repository.get_all_transactions()
        if transactions:
            transaction_id = transactions[0].id
            initial_count = len(repository.get_all_transactions())
            repository.delete(transaction_id)
            new_count = len(repository.get_all_transactions())
            assert new_count == initial_count - 1
