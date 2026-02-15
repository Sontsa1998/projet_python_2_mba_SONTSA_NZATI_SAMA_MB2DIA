"""Pagination utilities for the Transaction API.

This module provides utilities for handling pagination in API responses,
including parameter validation and paginated response creation.

Classes
-------
PaginationService
    Service for handling pagination operations.

Functions
---------
validate_pagination_params(page, limit)
    Validate pagination parameters.
create_paginated_response(data, page, limit, total_count)
    Create a paginated response with metadata.
"""

from typing import Generic, List, TypeVar

from transaction_api.config import MAX_LIMIT, MIN_LIMIT
from transaction_api.exceptions import InvalidPaginationParameters
from transaction_api.models import PaginatedResponse, PaginationMetadata

T = TypeVar("T")


class PaginationService(Generic[T]):
    """Service for handling pagination.
    
    Provides static methods for validating pagination parameters and creating
    paginated responses with appropriate metadata.
    """

    @staticmethod
    def validate_pagination_params(page: int, limit: int) -> tuple[int, int]:
        """Validate pagination parameters.
        
        Validates that page and limit parameters are within acceptable ranges
        as defined in the configuration.
        
        Parameters
        ----------
        page : int
            The page number (1-indexed).
        limit : int
            The number of items per page.
        
        Returns
        -------
        tuple[int, int]
            Tuple of (page, limit) if validation passes.
        
        Raises
        ------
        InvalidPaginationParameters
            If page is less than 1 or limit is outside the allowed range.
        
        Examples
        --------
        >>> page, limit = PaginationService.validate_pagination_params(1, 50)
        >>> page, limit
        (1, 50)
        """
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
        """Create a paginated response.
        
        Creates a paginated response object with the provided data and
        automatically calculated pagination metadata.
        
        Parameters
        ----------
        data : List[T]
            List of items for the current page.
        page : int
            Current page number (1-indexed).
        limit : int
            Number of items per page.
        total_count : int
            Total number of items across all pages.
        
        Returns
        -------
        PaginatedResponse[T]
            Paginated response with data and pagination metadata.
        
        Examples
        --------
        >>> items = [item1, item2, item3]
        >>> response = PaginationService.create_paginated_response(
        ...     items, page=1, limit=50, total_count=100
        ... )
        >>> response.pagination.has_next_page
        True
        """
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
