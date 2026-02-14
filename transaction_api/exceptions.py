"""Custom exceptions for the Transaction API."""


class TransactionAPIException(Exception):
    """Base exception for Transaction API."""

    pass

class TransactionNotFound(TransactionAPIException):
    """Exception raised when a transaction is not found."""

    pass
