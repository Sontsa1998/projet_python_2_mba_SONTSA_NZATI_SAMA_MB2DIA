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