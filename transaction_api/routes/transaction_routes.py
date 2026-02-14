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

