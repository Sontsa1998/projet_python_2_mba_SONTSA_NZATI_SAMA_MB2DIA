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


@router.get("", response_model=PaginatedResponse[CustomerSummary])
async def get_all_customers(
    page: int = Query(1, ge=1),
    limit: int = Query(50, ge=1, le=1000),
) -> PaginatedResponse[CustomerSummary]:
    """Get all customers with pagination."""
    try:
        service = get_service()
        return service.get_all_customers(page=page, limit=limit)
    except Exception as e:
        logger.error(f"Error getting customers: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving customers",
        )


@router.get("/{customer_id}", response_model=Customer)
async def get_customer_details(customer_id: str) -> Customer:
    """Get details for a specific customer."""
    try:
        service = get_service()
        return service.get_customer_details(customer_id)
    except Exception as e:
        logger.error(f"Error getting customer details: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving customer details",
        )


@router.get("/Ranked/top", response_model=list[TopCustomer])
async def get_top_customers(
    n: int = Query(
        10,
        ge=1,
        le=1000,
        description="Number of top customers",
    ),
) -> list[TopCustomer]:
    """Get top n customers by transaction count."""
    try:
        service = get_service()
        return service.get_top_customers(n=n)
    except Exception as e:
        logger.error(f"Error getting top customers: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving top customers",
        )
