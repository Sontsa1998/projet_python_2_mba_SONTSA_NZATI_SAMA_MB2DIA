"""Routes de l'API des statistiques.

Ce module définit tous les points de terminaison (endpoints) de l'API pour les opérations
de statistiques, y compris les statistiques générales, la distribution des montants,
les statistiques par type et les statistiques quotidiennes.

Fonctions
---------
get_service()
    Obtenir une instance du service de statistiques.
get_overview_stats()
    Récupérer les statistiques générales.
get_amount_distribution()
    Récupérer la distribution des montants.
get_stats_by_type()
    Récupérer les statistiques par type de transaction.
get_daily_stats()
    Récupérer les statistiques quotidiennes.
"""

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


def get_service() -> StatisticsService:
    """Obtenir une instance du service de statistiques.
    
    Retours
    -------
    StatisticsService
        Instance du service de statistiques.
    
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
    return StatisticsService(app_context.repository)


@router.get("/overview", response_model=OverviewStats)
async def get_overview_stats() -> OverviewStats:
    """Récupérer les statistiques générales.
    
    Retours
    -------
    OverviewStats
        Objet contenant les statistiques générales.
    
    Lève
    ----
    HTTPException
        En cas d'erreur lors de la récupération.
    """
    try:
        service = get_service()
        return service.get_overview_stats()
    except Exception as e:
        logger.error(f"Error getting overview stats: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving overview statistics",
        )


@router.get("/amount-distribution", response_model=AmountDistribution)
async def get_amount_distribution() -> AmountDistribution:
    """Récupérer les statistiques de distribution des montants.
    
    Retours
    -------
    AmountDistribution
        Objet contenant la distribution des montants par plages.
    
    Lève
    ----
    HTTPException
        En cas d'erreur lors de la récupération.
    """
    try:
        service = get_service()
        return service.get_amount_distribution()
    except Exception as e:
        logger.error(f"Error getting amount distribution: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving amount distribution",
        )


@router.get("/by-type", response_model=list[TypeStats])
async def get_stats_by_type() -> list[TypeStats]:
    """Récupérer les statistiques groupées par type de transaction.
    
    Retours
    -------
    list[TypeStats]
        Liste des statistiques par type de transaction.
    
    Lève
    ----
    HTTPException
        En cas d'erreur lors de la récupération.
    """
    try:
        service = get_service()
        return service.get_stats_by_type()
    except Exception as e:
        logger.error(f"Error getting stats by type: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving statistics by type",
        )


@router.get("/daily", response_model=list[dict])
async def get_daily_stats() -> list[dict]:
    """Récupérer les statistiques quotidiennes groupées par date.
    
    Retours
    -------
    list[dict]
        Liste des statistiques quotidiennes.
    
    Lève
    ----
    HTTPException
        En cas d'erreur lors de la récupération.
    """
    try:
        service = get_service()
        return service.get_daily_stats()
    except Exception as e:
        logger.error(f"Error getting daily stats: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving daily statistics",
        )
