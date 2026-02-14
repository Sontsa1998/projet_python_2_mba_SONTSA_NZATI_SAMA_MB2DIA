"""Pagination utilities for the Transaction API."""

from typing import Generic, List, TypeVar

from transaction_api.config import MAX_LIMIT, MIN_LIMIT
from transaction_api.exceptions import InvalidPaginationParameters
from transaction_api.models import PaginatedResponse, PaginationMetadata

T = TypeVar("T")