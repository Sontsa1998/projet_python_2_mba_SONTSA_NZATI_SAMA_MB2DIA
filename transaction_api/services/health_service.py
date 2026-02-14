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