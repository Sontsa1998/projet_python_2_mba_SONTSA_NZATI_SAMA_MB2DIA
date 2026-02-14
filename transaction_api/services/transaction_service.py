"""Transaction service for business logic."""

from typing import List

from transaction_api.exceptions import (
    InvalidPaginationParameters,
    TransactionNotFound,
)
from transaction_api.logging_config import get_logger
from transaction_api.models import (
    PaginatedResponse,
    SearchFilters,
    Transaction,
)
from transaction_api.pagination import PaginationService
from transaction_api.repository import TransactionRepository

logger = get_logger(__name__)


class TransactionService:
    """Service for transaction operations."""

    def __init__(self, repository: TransactionRepository) -> None:
        """Initialize the service."""
        self.repository = repository

    def get_all_transactions(
        self, page: int = 1, limit: int = 50
    ) -> PaginatedResponse[Transaction]:
        """Get all transactions with pagination."""
        try:
            page, limit = PaginationService.validate_pagination_params(
                page, limit
            )
        except InvalidPaginationParameters as e:
            logger.error(f"Invalid pagination parameters: {e}")
            raise

        transactions, total_count = self.repository.get_all(
            page=page, limit=limit
        )
        return PaginationService.create_paginated_response(
            transactions, page, limit, total_count
        )
    
    def get_transaction_by_id(self, transaction_id: str) -> Transaction:
        """Get a transaction by ID."""
        transaction = self.repository.get_by_id(transaction_id)
        if transaction is None:
            logger.warning(f"Transaction not found: {transaction_id}")
            msg = f"Transaction with ID {transaction_id} not found"
            raise TransactionNotFound(msg)
        return transaction

    def search_transactions(
        self, filters: SearchFilters, page: int = 1, limit: int = 50
    ) -> PaginatedResponse[Transaction]:
        """Search transactions with filters."""
        try:
            page, limit = PaginationService.validate_pagination_params(
                page, limit
            )
        except InvalidPaginationParameters as e:
            logger.error(f"Invalid pagination parameters: {e}")
            raise
        transactions, total_count = self.repository.search(
            filters=filters, page=page, limit=limit
        )
        return PaginationService.create_paginated_response(
            transactions, page, limit, total_count
        )
    
    def delete_transaction(self, transaction_id: str) -> None:
        """Delete a transaction."""
        transaction = self.repository.get_by_id(transaction_id)
        if transaction is None:
            logger.warning(
                "Transaction not found for deletion: %s",
                transaction_id,
            )
            msg = f"Transaction with ID {transaction_id} not found"
            raise TransactionNotFound(msg)

        self.repository.delete(transaction_id)
        logger.info(f"Deleted transaction: {transaction_id}")
