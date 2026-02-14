"""Transaction API routes."""

from fastapi import (
    APIRouter,
    HTTPException,
    Query,
    status,
)

from transaction_api import app_context
from transaction_api.exceptions import (
    InvalidPaginationParameters,
    TransactionNotFound,
)

from transaction_api.logging_config import get_logger
from transaction_api.models import (
    PaginatedResponse,
    SearchFilters,
    Transaction,
)

from transaction_api.services.transaction_service import TransactionService

logger = get_logger(__name__)

router: APIRouter = APIRouter(prefix="/api/transaction", tags=["transactions"])

def get_service() -> TransactionService:
    """Get transaction service instance."""
    if app_context.repository is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Repository not initialized",
        )
    return TransactionService(app_context.repository)

@router.get("", response_model=PaginatedResponse[Transaction])
async def get_all_transactions(
    page: int = Query(1, ge=1),
    limit: int = Query(50, ge=1, le=1000),
) -> PaginatedResponse[Transaction]:
    """Get all transactions with pagination."""
    try:
        service = get_service()
        return service.get_all_transactions(page=page, limit=limit)
    except InvalidPaginationParameters as e:
        logger.error(f"Invalid pagination parameters: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    except Exception as e:
        logger.error(f"Error getting transactions: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving transactions",
        )


@router.get("/{transaction_id}", response_model=Transaction)
async def get_transaction(transaction_id: str) -> Transaction:
    """Get a transaction by ID."""
    try:
        service = get_service()
        return service.get_transaction_by_id(transaction_id)
    except TransactionNotFound as e:
        logger.warning(f"Transaction not found: {transaction_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
    except Exception as e:
        logger.error(f"Error getting transaction: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving transaction",
        )

@router.delete("/{transaction_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_transaction(transaction_id: str) -> None:
    """Delete a transaction."""
    try:
        service = get_service()
        service.delete_transaction(transaction_id)
    except TransactionNotFound as e:
        logger.warning(f"Transaction not found for deletion: {transaction_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
    except Exception as e:
        logger.error(f"Error deleting transaction: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error deleting transaction",
        )


@router.post(
    "/transactionResearch/search",
    response_model=PaginatedResponse[Transaction],
)
async def search_transactions(
    filters: SearchFilters,
    page: int = Query(1, ge=1),
    limit: int = Query(50, ge=1, le=1000),
) -> PaginatedResponse[Transaction]:
    """Search transactions with multi-criteria filters."""
    try:
        service = get_service()
        return service.search_transactions(
            filters=filters, page=page, limit=limit
        )
    except InvalidPaginationParameters as e:
        logger.error(f"Invalid pagination parameters: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    except Exception as e:
        logger.error(f"Error searching transactions: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error searching transactions",
        )

@router.get(
    "/Type/types",
    response_model=list[dict],
)
async def get_transaction_types() -> list[dict]:
    """Get all transaction types with counts."""
    try:
        service = get_service()
        return service.get_transaction_types()
    except Exception as e:
        logger.error(f"Error getting transaction types: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving transaction types",
        )

@router.get(
    "/Latest/recent",
    response_model=PaginatedResponse[Transaction],
)
async def get_recent_transactions(
    limit: int = Query(50, ge=1, le=1000),
) -> PaginatedResponse[Transaction]:
    """Get recent transactions."""
    try: