"""Main FastAPI application."""

from contextlib import asynccontextmanager
from datetime import datetime

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from transaction_api import app_context
from transaction_api.config import API_DESCRIPTION, API_TITLE, API_VERSION
from transaction_api.exceptions import (
    CustomerNotFound,
    InvalidPaginationParameters,
    InvalidSearchFilters,
    TransactionNotFound,
)
from transaction_api.logging_config import get_logger, setup_logging
from transaction_api.repository import TransactionRepository
from transaction_api.routes import (
    transaction_routes as transaction_routes_mod,
    statistics_routes as statistics_routes_mod,
    fraud_routes as fraud_routes_mod,
    customer_routes as customer_routes_mod,
    system_routes as system_routes_mod,
)

transaction_router = transaction_routes_mod.router
statistics_router = statistics_routes_mod.router
fraud_router = fraud_routes_mod.router
customer_router = customer_routes_mod.router
system_router = system_routes_mod.router

# Set up logging
setup_logging()
logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for FastAPI app."""
    logger.info("Starting Transaction API")
    app_context.repository = TransactionRepository()
    try:
        logger.info("Loading transaction data from CSV")
        app_context.repository.load_from_csv()
        total_transactions = len(app_context.repository.get_all_transactions())
        logger.info(f"Successfully loaded {total_transactions} transactions")
    except Exception as e:
        logger.error(f"Failed to load transaction data: {e}")
        raise
    yield
    logger.info("Shutting down Transaction API")


# Create FastAPI app
app = FastAPI(
    title=API_TITLE,
    description=API_DESCRIPTION,
    version=API_VERSION,
    lifespan=lifespan,
)


@app.exception_handler(TransactionNotFound)
async def transaction_not_found_handler(
    request: Request, exc: TransactionNotFound
):
    """Handle TransactionNotFound exception."""
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            "error": "Transaction not found",
            "details": str(exc),
            "timestamp": datetime.utcnow().isoformat(),
        },
    )


@app.exception_handler(CustomerNotFound)
async def customer_not_found_handler(request: Request, exc: CustomerNotFound):
    """Handle CustomerNotFound exception."""
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            "error": "Customer not found",
            "details": str(exc),
            "timestamp": datetime.utcnow().isoformat(),
        },
    )


@app.exception_handler(InvalidPaginationParameters)
async def invalid_pagination_handler(
    request: Request,
    exc: InvalidPaginationParameters,
):
    """Handle InvalidPaginationParameters exception."""
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "error": "Invalid pagination parameters",
            "details": str(exc),
            "timestamp": datetime.utcnow().isoformat(),
        },
    )


@app.exception_handler(InvalidSearchFilters)
async def invalid_search_filters_handler(
    request: Request, exc: InvalidSearchFilters
):
    """Handle InvalidSearchFilters exception."""
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "error": "Invalid search filters",
            "details": str(exc),
            "timestamp": datetime.utcnow().isoformat(),
        },
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle general exceptions."""
    logger.error(f"Unexpected error: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Internal server error",
            "details": "An unexpected error occurred",
            "timestamp": datetime.utcnow().isoformat(),
        },
    )