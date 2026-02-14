"""Pagination utilities for the Transaction API."""

from typing import Generic, List, TypeVar

from transaction_api.config import MAX_LIMIT, MIN_LIMIT
from transaction_api.exceptions import InvalidPaginationParameters
from transaction_api.models import PaginatedResponse, PaginationMetadata

T = TypeVar("T")

class PaginationService(Generic[T]):
    """Service for handling pagination."""

    @staticmethod
    def validate_pagination_params(page: int, limit: int) -> tuple[int, int]:
        """Validate pagination parameters."""
        if page < 1:
            raise InvalidPaginationParameters("Page must be >= 1")
        if limit < MIN_LIMIT or limit > MAX_LIMIT:
            raise InvalidPaginationParameters(
                f"Limit must be between {MIN_LIMIT} and {MAX_LIMIT}"
            )
        return page, limit
