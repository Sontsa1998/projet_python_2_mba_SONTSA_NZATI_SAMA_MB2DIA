"""Customer API routes."""

from fastapi import (
    APIRouter,
    HTTPException,
    Query,
    status,
)

from transaction_api import app_context
from transaction_api.logging_config import get_logger
from transaction_api.models import (
    Customer,
    CustomerSummary,
    PaginatedResponse,
    TopCustomer,
)
from transaction_api.services.customer_service import CustomerService

logger = get_logger(__name__)

router: APIRouter = APIRouter(prefix="/api/customers", tags=["customers"])


def get_service() -> CustomerService:
    """Get customer service instance."""
    if app_context.repository is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Repository not initialized",
        )
    return CustomerService(app_context.repository)
