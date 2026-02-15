"""Routes de l'API de détection de fraude.

Ce module définit tous les points de terminaison (endpoints) de l'API pour les opérations
de détection de fraude, y compris le résumé de fraude, les statistiques par type et
la prédiction de fraude.

Fonctions
---------
get_service()
    Obtenir une instance du service de fraude.
get_fraud_summary()
    Récupérer le résumé de la détection de fraude.
get_fraud_by_type()
    Récupérer les statistiques de fraude par type.
predict_fraud(transaction)
    Prédire le risque de fraude pour une transaction.
"""

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
    """Obtenir une instance du service de fraude.
    
    Retours
    -------
    FraudService
        Instance du service de fraude.
    
    Lève
    ----
    HTTPException
        Si le référentiel n'est pas initialisé.
    """
    if app_context.repository is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Repository not initialized",
        )
    return FraudService(app_context.repository)

@router.get("/summary", response_model=FraudSummary)
async def get_fraud_summary() -> FraudSummary:
    """Récupérer le résumé de la détection de fraude.
    
    Retours
    -------
    FraudSummary
        Résumé contenant les statistiques de fraude.
    
    Lève
    ----
    HTTPException
        En cas d'erreur lors de la récupération.
    """
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
    """Récupérer les statistiques de fraude groupées par type de transaction.
    
    Retours
    -------
    list[FraudTypeStats]
        Liste des statistiques de fraude par type de transaction.
    
    Lève
    ----
    HTTPException
        En cas d'erreur lors de la récupération.
    """
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
    """Prédire le risque de fraude pour une transaction.
    
    Paramètres
    ----------
    transaction : Transaction
        La transaction à analyser.
    
    Retours
    -------
    FraudPrediction
        Prédiction contenant le score de fraude et le raisonnement.
    
    Lève
    ----
    HTTPException
        En cas d'erreur lors de la prédiction.
    """
    try:
        service = get_service()
        return service.predict_fraud(transaction)
    except Exception as e:
        logger.error(f"Error predicting fraud: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error predicting fraud",
        )
