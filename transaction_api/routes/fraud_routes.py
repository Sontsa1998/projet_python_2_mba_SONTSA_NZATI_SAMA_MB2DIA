"""Fraud detection API routes."""

from fastapi import APIRouter, HTTPException, status

from transaction_api import app_context
from transaction_api.logging_config import get_logger
from transaction_api.models import (
    FraudPrediction,
    FraudSummary,
    FraudTypeStats,
    Transaction,
)
from transaction_api.services.fraud_service import FraudService

logger = get_logger(__name__)

router: APIRouter = APIRouter(prefix="/api/fraud", tags=["fraud"])

def get_service() -> FraudService:
    """Get fraud service instance."""
    if app_context.repository is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Repository not initialized",
        )
    return FraudService(app_context.repository)

@router.get("/summary", response_model=FraudSummary)
async def get_fraud_summary() -> FraudSummary:
    """Get fraud detection summary."""
    try:
        service = get_service()
        return service.get_fraud_summary()
    except Exception as e:
        logger.error(f"Error getting fraud summary: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving fraud summary",
        )

@router.get("/by-type", response_model=list[FraudTypeStats])
async def get_fraud_by_type() -> list[FraudTypeStats]:
    """Get fraud statistics grouped by use_chip type."""
    try:
        service = get_service()
        return service.get_fraud_by_type()
    except Exception as e:
        logger.error(f"Error getting fraud by use_chip type: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving fraud statistics by use_chip type",
        )


@router.post("/predict", response_model=FraudPrediction)
async def predict_fraud(transaction: Transaction) -> FraudPrediction:
    """Predict fraud risk for a transaction."""
    try:
        service = get_service()
        return service.predict_fraud(transaction)
    except Exception as e:
        logger.error(f"Error predicting fraud: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error predicting fraud",
        )
