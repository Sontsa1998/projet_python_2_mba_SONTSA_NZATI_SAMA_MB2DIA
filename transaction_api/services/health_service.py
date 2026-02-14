"""Health and metadata service for business logic."""

import time
from datetime import datetime

from transaction_api.config import API_VERSION
from transaction_api.logging_config import get_logger
from transaction_api.models import HealthStatus, SystemMetadata
from transaction_api.repository import TransactionRepository

logger = get_logger(__name__)

class HealthService:
    """Service for health checks and metadata."""

    def __init__(self, repository: TransactionRepository) -> None:
        """Initialize the service."""
        self.repository = repository
    
    def check_health(self) -> HealthStatus:
        """Check system health."""
        start_time = time.time()

        try:
            # Simple health check - verify repository is accessible
            _ = self.repository.get_all_transactions()

            response_time_ms = (time.time() - start_time) * 1000
            return HealthStatus(
                status="healthy",
                response_time_ms=response_time_ms,
            )
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            response_time_ms = (time.time() - start_time) * 1000
            return HealthStatus(
                status="unhealthy",
                response_time_ms=response_time_ms,
            )