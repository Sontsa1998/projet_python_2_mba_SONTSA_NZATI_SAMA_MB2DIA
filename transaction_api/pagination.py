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

    @staticmethod
    def create_paginated_response(
        data: List[T], page: int, limit: int, total_count: int
    ) -> PaginatedResponse[T]:
        """Create a paginated response."""
        total_pages = (total_count + limit - 1) // limit
        has_next_page = page < total_pages

        pagination_metadata = PaginationMetadata(
            page=page,
            limit=limit,
            total_count=total_count,
            total_pages=total_pages,
            has_next_page=has_next_page,
        )

        return PaginatedResponse(data=data, pagination=pagination_metadata)
