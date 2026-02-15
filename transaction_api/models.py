"""Pydantic models for the Transaction API.

This module defines all Pydantic data models used throughout the Transaction API,
including transaction data, pagination metadata, statistics, fraud detection,
and customer information models.

Classes
-------
Transaction
    Represents a single transaction record with all associated details.
PaginationMetadata
    Contains pagination information for paginated responses.
PaginatedResponse
    Generic paginated response wrapper for any data type.
OverviewStats
    Overview statistics for all transactions.
AmountBucket
    Represents a bucket in amount distribution analysis.
AmountDistribution
    Amount distribution statistics across buckets.
TypeStats
    Statistics for a specific transaction type.
DailyStats
    Daily transaction statistics.
FraudSummary
    Summary of fraud detection results.
FraudTypeStats
    Fraud statistics broken down by transaction type.
FraudUseChipStats
    Fraud statistics broken down by use_chip type.
FraudPrediction
    Result of fraud prediction for a transaction.
Customer
    Customer details and transaction summary.
TopCustomer
    Summary of a top customer by transaction volume.
CustomerSummary
    Basic customer summary information.
HealthStatus
    System health status information.
SystemMetadata
    System-wide metadata and statistics.
ErrorResponse
    Standard error response format.
SearchFilters
    Search filter parameters for transaction queries.
"""

from datetime import date as date_type
from datetime import datetime
from typing import Generic, List, Optional, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


class Transaction(BaseModel):
    """Transaction data model.
    
    Represents a single transaction record with all associated details including
    date, customer information, card details, merchant information, and amount.
    
    Attributes
    ----------
    id : str
        Unique transaction identifier.
    date : datetime
        Date and time when the transaction occurred.
    client_id : str
        Identifier of the client/customer making the transaction.
    card_id : str
        Identifier of the card used for the transaction.
    amount : float
        Transaction amount in currency units.
    use_chip : str
        Type of transaction (e.g., "Swipe Transaction", "Chip Transaction").
    merchant_id : str
        Identifier of the merchant where transaction occurred.
    merchant_city : str
        City where the merchant is located.
    merchant_state : str
        State/province where the merchant is located.
    zip : str
        ZIP/postal code of the merchant location.
    mcc : str
        Merchant Category Code for classification.
    errors : str, optional
        Error flag indicating if transaction has errors.
    
    Examples
    --------
    >>> transaction = Transaction(
    ...     id="1",
    ...     date=datetime(2023, 1, 1, 12, 0, 0),
    ...     client_id="C001",
    ...     card_id="CARD001",
    ...     amount=100.50,
    ...     use_chip="Swipe Transaction",
    ...     merchant_id="M001",
    ...     merchant_city="New York",
    ...     merchant_state="NY",
    ...     zip="10001",
    ...     mcc="5411",
    ...     errors=None
    ... )
    """

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
        """Pydantic configuration for Transaction model.
        
        Provides JSON schema example for API documentation.
        """

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
    """Pagination metadata.
    
    Contains information about pagination state including current page,
    limit, total counts, and navigation indicators.
    
    Attributes
    ----------
    page : int
        Current page number (1-indexed).
    limit : int
        Number of items per page.
    total_count : int
        Total number of items across all pages.
    total_pages : int
        Total number of pages available.
    has_next_page : bool
        Whether there is a next page available.
    """

    page: int = Field(..., description="Current page number")
    limit: int = Field(..., description="Items per page")
    total_count: int = Field(..., description="Total items")
    total_pages: int = Field(..., description="Total pages")
    has_next_page: bool = Field(..., description="Has next page")


class PaginatedResponse(BaseModel, Generic[T]):
    """Generic paginated response.
    
    Wraps a list of items with pagination metadata for paginated API responses.
    
    Attributes
    ----------
    data : List[T]
        List of items for the current page.
    pagination : PaginationMetadata
        Pagination information and navigation details.
    
    Examples
    --------
    >>> response = PaginatedResponse(
    ...     data=[item1, item2],
    ...     pagination=PaginationMetadata(
    ...         page=1, limit=50, total_count=100,
    ...         total_pages=2, has_next_page=True
    ...     )
    ... )
    """

    data: List[T] = Field(..., description="List of items")
    pagination: PaginationMetadata = Field(..., description="Pagination info")


class OverviewStats(BaseModel):
    """Overview statistics.
    
    Provides high-level statistics about all transactions in the system.
    
    Attributes
    ----------
    total_count : int
        Total number of transactions.
    total_amount : float
        Sum of all transaction amounts.
    average_amount : float
        Average transaction amount.
    min_date : datetime
        Earliest transaction date.
    max_date : datetime
        Latest transaction date.
    """

    total_count: int = Field(..., description="Total transactions")
    total_amount: float = Field(..., description="Total amount")
    average_amount: float = Field(..., description="Average amount")
    min_date: datetime = Field(..., description="Earliest date")
    max_date: datetime = Field(..., description="Latest date")


class AmountBucket(BaseModel):
    """Amount distribution bucket.
    
    Represents a single bucket in the amount distribution analysis.
    
    Attributes
    ----------
    range : str
        Label describing the amount range (e.g., "0-100").
    count : int
        Number of transactions in this bucket.
    percentage : float
        Percentage of total transactions in this bucket.
    """

    range: str = Field(..., description="Range label")
    count: int = Field(..., description="Bucket count")
    percentage: float = Field(..., description="Percentage of total")


class AmountDistribution(BaseModel):
    """Amount distribution statistics.
    
    Contains distribution of transactions across amount buckets.
    
    Attributes
    ----------
    buckets : List[AmountBucket]
        List of amount distribution buckets.
    """

    buckets: List[AmountBucket] = Field(..., description="Buckets")


class TypeStats(BaseModel):
    """Statistics for a transaction type.
    
    Provides statistics for a specific transaction type.
    
    Attributes
    ----------
    type : str
        Transaction type identifier.
    count : int
        Number of transactions of this type.
    total_amount : float
        Sum of amounts for this transaction type.
    average_amount : float
        Average amount for this transaction type.
    """

    type: str = Field(..., description="Transaction type")
    count: int = Field(..., description="Count")
    total_amount: float = Field(..., description="Total amount")
    average_amount: float = Field(..., description="Average amount")


class DailyStats(BaseModel):
    """Daily statistics.
    
    Provides transaction statistics for a specific day.
    
    Attributes
    ----------
    date : date_type
        The date for these statistics.
    count : int
        Number of transactions on this date.
    total_amount : float
        Sum of transaction amounts on this date.
    average_amount : float
        Average transaction amount on this date.
    """

    date: date_type = Field(..., description="Date")
    count: int = Field(..., description="Count")
    total_amount: float = Field(..., description="Total amount")
    average_amount: float = Field(..., description="Average amount")


class FraudSummary(BaseModel):
    """Fraud detection summary.
    
    Provides overall fraud detection statistics.
    
    Attributes
    ----------
    total_fraud_count : int
        Total number of fraudulent transactions detected.
    fraud_rate : float
        Percentage of transactions flagged as fraudulent.
    total_fraud_amount : float
        Sum of amounts in fraudulent transactions.
    """

    total_fraud_count: int = Field(..., description="Fraud count")
    fraud_rate: float = Field(..., description="Fraud rate")
    total_fraud_amount: float = Field(..., description="Fraud amount")


class FraudTypeStats(BaseModel):
    """Fraud statistics by type.
    
    Provides fraud statistics broken down by transaction type.
    
    Attributes
    ----------
    type : str
        Transaction type identifier.
    fraud_count : int
        Number of fraudulent transactions of this type.
    fraud_rate : float
        Fraud rate for this transaction type.
    total_count : int
        Total transactions of this type.
    """

    type: str = Field(..., description="Transaction type")
    fraud_count: int = Field(..., description="Fraud count")
    fraud_rate: float = Field(..., description="Fraud rate")
    total_count: int = Field(..., description="Total count")


class FraudUseChipStats(BaseModel):
    """Fraud statistics by use_chip type.
    
    Provides fraud statistics broken down by use_chip type.
    
    Attributes
    ----------
    use_chip : str
        Use chip type identifier.
    fraud_count : int
        Number of fraudulent transactions of this use_chip type.
    fraud_rate : float
        Fraud rate for this use_chip type.
    total_count : int
        Total transactions of this use_chip type.
    """

    use_chip: str = Field(..., description="use_chip type")
    fraud_count: int = Field(..., description="Fraud count")
    fraud_rate: float = Field(..., description="Fraud rate")
    total_count: int = Field(..., description="Total count")


class FraudPrediction(BaseModel):
    """Fraud prediction result.
    
    Contains the result of fraud prediction for a transaction.
    
    Attributes
    ----------
    fraud_score : float
        Fraud probability score between 0.0 and 1.0.
    reasoning : str
        Explanation of the fraud prediction.
    """

    fraud_score: float = Field(..., ge=0.0, le=1.0, description="Fraud score")
    reasoning: str = Field(..., description="Reasoning")


class Customer(BaseModel):
    """Customer details.
    
    Provides detailed information about a customer and their transactions.
    
    Attributes
    ----------
    customer_id : str
        Unique customer identifier.
    transaction_count : int
        Total number of transactions by this customer.
    total_amount : float
        Sum of all transaction amounts by this customer.
    average_amount : float
        Average transaction amount for this customer.
    """

    customer_id: str = Field(..., description="Customer id")
    transaction_count: int = Field(..., description="Transaction count")
    total_amount: float = Field(..., description="Total amount")
    average_amount: float = Field(..., description="Average amount")


class TopCustomer(BaseModel):
    """Top customer summary.
    
    Summary information for a top customer by transaction volume.
    
    Attributes
    ----------
    customer_id : str
        Unique customer identifier.
    transaction_count : int
        Number of transactions by this customer.
    total_amount : float
        Sum of transaction amounts by this customer.
    """

    customer_id: str = Field(..., description="Customer id")
    transaction_count: int = Field(..., description="Transaction count")
    total_amount: float = Field(..., description="Total transaction amount")


class CustomerSummary(BaseModel):
    """Customer summary.
    
    Basic summary information for a customer.
    
    Attributes
    ----------
    customer_id : str
        Unique customer identifier.
    transaction_count : int
        Number of transactions by this customer.
    """

    customer_id: str = Field(..., description="Customer id")
    transaction_count: int = Field(..., description="Transaction count")


class HealthStatus(BaseModel):
    """System health status.
    
    Indicates the current health status of the system.
    
    Attributes
    ----------
    status : str
        Health status indicator (e.g., "healthy", "degraded").
    response_time_ms : float
        Response time in milliseconds.
    """

    status: str = Field(..., description="Health status")
    response_time_ms: float = Field(..., description="Response time ms")


class SystemMetadata(BaseModel):
    """System metadata.
    
    Contains system-wide metadata and statistics.
    
    Attributes
    ----------
    total_transaction_count : int
        Total number of transactions in the system.
    data_load_date : datetime
        When the transaction data was loaded.
    api_version : str
        Current API version.
    min_date : datetime
        Earliest transaction date in the system.
    max_date : datetime
        Latest transaction date in the system.
    """

    total_transaction_count: int = Field(..., description="Total transactions")
    data_load_date: datetime = Field(..., description="Data load date")
    api_version: str = Field(..., description="API version")
    min_date: datetime = Field(..., description="Earliest date")
    max_date: datetime = Field(..., description="Latest date")


class ErrorResponse(BaseModel):
    """Error response.
    
    Standard format for error responses from the API.
    
    Attributes
    ----------
    error : str
        Error message.
    details : str, optional
        Additional error details.
    timestamp : datetime
        When the error occurred.
    """

    error: str = Field(..., description="Error message")
    details: Optional[str] = Field(None, description="Details")
    timestamp: datetime = Field(..., description="Timestamp")


class SearchFilters(BaseModel):
    """Search filters for transactions.
    
    Defines optional filters for transaction search queries.
    
    Attributes
    ----------
    min_amount : float, optional
        Minimum transaction amount filter.
    max_amount : float, optional
        Maximum transaction amount filter.
    client_id : str, optional
        Filter by client/customer ID.
    transaction_id : str, optional
        Filter by transaction ID.
    merchant_city : str, optional
        Filter by merchant city.
    use_chip : str, optional
        Filter by transaction type.
    """

    min_amount: Optional[float] = Field(None, description="Min amount")
    max_amount: Optional[float] = Field(None, description="Max amount")
    client_id: Optional[str] = Field(None, description="Client id")
    transaction_id: Optional[str] = Field(None, description="Transaction id")
    merchant_city: Optional[str] = Field(None, description="Merchant city")
    use_chip: Optional[str] = Field(None, description="Transaction type")
