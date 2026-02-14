"""System API routes."""

from fastapi import APIRouter, HTTPException, status

from transaction_api import app_context
from transaction_api.logging_config import get_logger
from transaction_api.models import HealthStatus, SystemMetadata
from transaction_api.services.health_service import HealthService

logger = get_logger(__name__)

router: APIRouter = APIRouter(prefix="/api/system", tags=["system"])


def get_service() -> HealthService:
    """Get health service instance."""
    if app_context.repository is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Repository not initialized",
        )
    return HealthService(app_context.repository)


@router.get("/health", response_model=HealthStatus)
async def get_health_status() -> HealthStatus:
    """Get system health status."""
    try:
        service = get_service()
        return service.check_health()
    except Exception as e:
        logger.error(f"Error checking health: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error checking system health",
        )
    

    