"""Custom exceptions for the Transaction API."""


class TransactionAPIException(Exception):
    """Base exception for Transaction API."""

    pass

class TransactionNotFound(TransactionAPIException):
    """Exception raised when a transaction is not found."""

    pass

class CustomerNotFound(TransactionAPIException):
    """Exception raised when a customer is not found."""

    pass

class InvalidPaginationParameters(TransactionAPIException):
    """Exception raised when pagination parameters are invalid."""

    pass

class InvalidSearchFilters(TransactionAPIException):
    """Exception raised when search filters are invalid."""

    pass

class DataLoadingError(TransactionAPIException):
    """Exception raised when data loading fails."""

    pass

class InvalidTransactionData(TransactionAPIException):
    """Exception raised when transaction data is invalid."""

    pass
