"""Statistics API routes."""

from fastapi import APIRouter, HTTPException, status

from transaction_api import app_context
from transaction_api.logging_config import get_logger
from transaction_api.models import (
    AmountDistribution,
    OverviewStats,
    TypeStats,
)
from transaction_api.services.statistics_service import StatisticsService

logger = get_logger(__name__)

router: APIRouter = APIRouter(prefix="/api/stats", tags=["statistics"])
