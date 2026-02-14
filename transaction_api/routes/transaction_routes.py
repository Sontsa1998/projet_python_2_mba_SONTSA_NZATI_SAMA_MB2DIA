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
