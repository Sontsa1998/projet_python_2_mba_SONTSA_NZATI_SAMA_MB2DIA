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