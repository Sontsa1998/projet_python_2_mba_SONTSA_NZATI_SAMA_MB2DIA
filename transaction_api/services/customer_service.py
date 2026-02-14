"""Customer service for business logic."""

from typing import List

from transaction_api.exceptions import InvalidPaginationParameters
from transaction_api.logging_config import get_logger
from transaction_api.models import (
    Customer,
    CustomerSummary,
    PaginatedResponse,
    TopCustomer,
)
from transaction_api.pagination import PaginationService
from transaction_api.repository import TransactionRepository

logger = get_logger(__name__)


class CustomerService:
    """Service for customer operations."""

    def __init__(self, repository: TransactionRepository) -> None:
        """Initialize the service."""
        self.repository = repository

    def get_all_customers(
        self, page: int = 1, limit: int = 50
    ) -> PaginatedResponse[CustomerSummary]:
        """Get all customers with pagination."""
        try:
            page, limit = PaginationService.validate_pagination_params(
                page, limit
            )
        except InvalidPaginationParameters as e:
            logger.error(f"Invalid pagination parameters: {e}")
            raise

        customer_ids = self.repository.get_all_customers()
        total_count = len(customer_ids)

        # Sort customer IDs for consistent pagination
        customer_ids = sorted(customer_ids)

        # Apply pagination
        offset = (page - 1) * limit
        paginated_ids = customer_ids[offset: offset + limit]

        # Create customer summaries
        customers = []
        for customer_id in paginated_ids:
            transaction_count = len(
                self.repository.get_by_customer(
                    customer_id, page=1, limit=1000000
                )[0]
            )
            customers.append(
                CustomerSummary(
                    customer_id=customer_id,
                    transaction_count=transaction_count,
                )
            )

        return PaginationService.create_paginated_response(
            customers, page, limit, total_count
        )
    
    def get_customer_details(self, customer_id: str) -> Customer:
        """Get details for a specific customer."""
        transactions, total_count = self.repository.get_by_customer(
            customer_id, page=1, limit=1000000
        )

        if not transactions:
            # Return empty customer
            return Customer(
                customer_id=customer_id,
                transaction_count=0,
                total_amount=0.0,
                average_amount=0.0,
            )

        total_amount = sum(t.amount for t in transactions)
        average_amount = (
            total_amount / len(transactions) if transactions else 0.0
        )

        return Customer(
            customer_id=customer_id,
            transaction_count=len(transactions),
            total_amount=total_amount,
            average_amount=average_amount,
        )
    
    