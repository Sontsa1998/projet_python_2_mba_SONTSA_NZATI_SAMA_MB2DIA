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


class OverviewStats(BaseModel):
    """Overview statistics."""

    total_count: int = Field(..., description="Total transactions")
    total_amount: float = Field(..., description="Total amount")
    average_amount: float = Field(..., description="Average amount")
    min_date: datetime = Field(..., description="Earliest date")
    max_date: datetime = Field(..., description="Latest date")


class AmountBucket(BaseModel):
    """Amount distribution bucket."""

    range: str = Field(..., description="Range label")
    count: int = Field(..., description="Bucket count")
    percentage: float = Field(..., description="Percentage of total")


class AmountDistribution(BaseModel):
    """Amount distribution statistics."""

    buckets: List[AmountBucket] = Field(..., description="Buckets")


class TypeStats(BaseModel):
    """Statistics for a transaction type."""

    type: str = Field(..., description="Transaction type")
    count: int = Field(..., description="Count")
    total_amount: float = Field(..., description="Total amount")
    average_amount: float = Field(..., description="Average amount")


class DailyStats(BaseModel):
    """Daily statistics."""

    date: date_type = Field(..., description="Date")
    count: int = Field(..., description="Count")
    total_amount: float = Field(..., description="Total amount")
    average_amount: float = Field(..., description="Average amount")


class FraudSummary(BaseModel):
    """Fraud detection summary."""

    total_fraud_count: int = Field(..., description="Fraud count")
    fraud_rate: float = Field(..., description="Fraud rate")
    total_fraud_amount: float = Field(..., description="Fraud amount")


class FraudTypeStats(BaseModel):
    """Fraud statistics by type."""

    type: str = Field(..., description="Transaction type")
    fraud_count: int = Field(..., description="Fraud count")
    fraud_rate: float = Field(..., description="Fraud rate")
    total_count: int = Field(..., description="Total count")


class FraudUseChipStats(BaseModel):
    """Fraud statistics by use_chip type."""

    use_chip: str = Field(..., description="use_chip type")
    fraud_count: int = Field(..., description="Fraud count")
    fraud_rate: float = Field(..., description="Fraud rate")
    total_count: int = Field(..., description="Total count")


class FraudPrediction(BaseModel):
    """Fraud prediction result."""

    fraud_score: float = Field(..., ge=0.0, le=1.0, description="Fraud score")
    reasoning: str = Field(..., description="Reasoning")


class Customer(BaseModel):
    """Customer details."""

    customer_id: str = Field(..., description="Customer id")
    transaction_count: int = Field(..., description="Transaction count")
    total_amount: float = Field(..., description="Total amount")
    average_amount: float = Field(..., description="Average amount")


class TopCustomer(BaseModel):
    """Top customer summary."""

    customer_id: str = Field(..., description="Customer id")
    transaction_count: int = Field(..., description="Transaction count")
    total_amount: float = Field(..., description="Total transaction amount")


class CustomerSummary(BaseModel):
    """Customer summary."""

    customer_id: str = Field(..., description="Customer id")
    transaction_count: int = Field(..., description="Transaction count")


class HealthStatus(BaseModel):
    """System health status."""

    status: str = Field(..., description="Health status")
    response_time_ms: float = Field(..., description="Response time ms")


class SystemMetadata(BaseModel):
    """System metadata."""

    total_transaction_count: int = Field(..., description="Total transactions")
    data_load_date: datetime = Field(..., description="Data load date")
    api_version: str = Field(..., description="API version")
    min_date: datetime = Field(..., description="Earliest date")
    max_date: datetime = Field(..., description="Latest date")


class ErrorResponse(BaseModel):
    """Error response."""

    error: str = Field(..., description="Error message")
    details: Optional[str] = Field(None, description="Details")
    timestamp: datetime = Field(..., description="Timestamp")


class SearchFilters(BaseModel):
    """Search filters for transactions."""

    min_amount: Optional[float] = Field(None, description="Min amount")
    max_amount: Optional[float] = Field(None, description="Max amount")
    client_id: Optional[str] = Field(None, description="Client id")
    transaction_id: Optional[str] = Field(None, description="Transaction id")
    merchant_city: Optional[str] = Field(None, description="Merchant city")
    use_chip: Optional[str] = Field(None, description="Transaction type")
