"""Custom exceptions for the Transaction API.

This module defines custom exception classes for the Transaction API, providing
specific error types for different failure scenarios in the application.

Classes
-------
TransactionAPIException
    Base exception class for all Transaction API exceptions.
TransactionNotFound
    Raised when a requested transaction cannot be found.
CustomerNotFound
    Raised when a requested customer cannot be found.
InvalidPaginationParameters
    Raised when pagination parameters are invalid.
InvalidSearchFilters
    Raised when search filter parameters are invalid.
DataLoadingError
    Raised when data loading from CSV fails.
InvalidTransactionData
    Raised when transaction data is invalid or malformed.
"""


class TransactionAPIException(Exception):
    """Base exception for Transaction API.
    
    This is the base exception class for all custom exceptions in the
    Transaction API. All other custom exceptions inherit from this class.
    """

    pass


class TransactionNotFound(TransactionAPIException):
    """Exception raised when a transaction is not found.
    
    This exception is raised when a transaction lookup fails because the
    requested transaction ID does not exist in the repository.
    """

    pass


class CustomerNotFound(TransactionAPIException):
    """Exception raised when a customer is not found.
    
    This exception is raised when a customer lookup fails because the
    requested customer ID does not exist in the repository.
    """

    pass


class InvalidPaginationParameters(TransactionAPIException):
    """Exception raised when pagination parameters are invalid.
    
    This exception is raised when pagination parameters (page, limit) are
    outside acceptable ranges or violate validation rules.
    """

    pass


class InvalidSearchFilters(TransactionAPIException):
    """Exception raised when search filters are invalid.
    
    This exception is raised when search filter parameters are malformed,
    contain invalid values, or violate business logic constraints.
    """

    pass


class DataLoadingError(TransactionAPIException):
    """Exception raised when data loading fails.
    
    This exception is raised when loading transaction data from the CSV file
    fails due to file I/O errors, parsing errors, or other data loading issues.
    """

    pass


class InvalidTransactionData(TransactionAPIException):
    """Exception raised when transaction data is invalid.
    
    This exception is raised when transaction data is malformed, missing required
    fields, or contains values that violate data validation rules.
    """

    pass
