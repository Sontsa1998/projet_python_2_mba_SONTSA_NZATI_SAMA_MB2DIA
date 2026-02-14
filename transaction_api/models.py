"""Pydantic models for the Transaction API."""

from datetime import date as date_type
from datetime import datetime
from typing import Generic, List, Optional, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


class Transaction(BaseModel):
    """Transaction data model."""

    id: str = Field(..., description="Transaction id")
    date: datetime = Field(..., description="Transaction date and time")
    client_id: str = Field(..., description="Client id")
    card_id: str = Field(..., description="Card id")
    amount: float = Field(..., description="Amount")
    use_chip: str = Field(..., description="Transaction type")
    merchant_id: str = Field(..., description="Merchant id")
    merchant_city: str = Field(..., description="Merchant city")
    merchant_state: str = Field(..., description="Merchant state")
    zip: str = Field(..., description="ZIP code")
    mcc: str = Field(..., description="Merchant category code")
    errors: Optional[str] = Field(None, description="Error flag")

    class Config:
        """Pydantic config."""

        json_schema_extra = {
            "example": {
                "id": "1",
                "date": "2023-01-01T12:00:00",
                "client_id": "C001",
                "card_id": "CARD001",
                "amount": 100.50,
                "use_chip": "Swipe Transaction",
                "merchant_id": "M001",
                "merchant_city": "New York",
                "merchant_state": "NY",
                "zip": "10001",
                "mcc": "5411",
                "errors": None,
            }
        }


class PaginationMetadata(BaseModel):
    """Pagination metadata."""

    page: int = Field(..., description="Current page number")
    limit: int = Field(..., description="Items per page")
    total_count: int = Field(..., description="Total items")
    total_pages: int = Field(..., description="Total pages")
    has_next_page: bool = Field(..., description="Has next page")


class PaginatedResponse(BaseModel, Generic[T]):
    """Generic paginated response."""

    data: List[T] = Field(..., description="List of items")
    pagination: PaginationMetadata = Field(..., description="Pagination info")


