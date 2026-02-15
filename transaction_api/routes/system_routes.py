"""Routes de l'API système.

Ce module définit tous les points de terminaison (endpoints) de l'API pour les opérations
système, y compris les vérifications de santé et la récupération des métadonnées.

Fonctions
---------
get_service()
    Obtenir une instance du service de santé.
get_health_status()
    Récupérer l'état de santé du système.
get_system_metadata()
    Récupérer les métadonnées du système.
"""

from fastapi import APIRouter, HTTPException, status

from transaction_api import app_context
from transaction_api.logging_config import get_logger
from transaction_api.models import HealthStatus, SystemMetadata
from transaction_api.services.health_service import HealthService

logger = get_logger(__name__)

router: APIRouter = APIRouter(prefix="/api/system", tags=["system"])


def get_service() -> HealthService:
    """Obtenir une instance du service de santé.
    
    Retours
    -------
    HealthService
        Instance du service de santé.
    
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
    return HealthService(app_context.repository)


@router.get("/health", response_model=HealthStatus)
async def get_health_status() -> HealthStatus:
    """Récupérer l'état de santé du système.
    
    Retours
    -------
    HealthStatus
        Objet contenant l'état de santé et le temps de réponse.
    
    Lève
    ----
    HTTPException
        En cas d'erreur lors de la vérification.
    """
    try:
        service = get_service()
        return service.check_health()
    except Exception as e:
        logger.error(f"Error checking health: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error checking system health",
        )


@router.get("/metadata", response_model=SystemMetadata)
async def get_system_metadata() -> SystemMetadata:
    """Récupérer les métadonnées du système.
    
    Retours
    -------
    SystemMetadata
        Objet contenant les métadonnées du système.
    
    Lève
    ----
    HTTPException
        En cas d'erreur lors de la récupération.
    """
    try:
        service = get_service()
        return service.get_metadata()
    except Exception as e:
        logger.error(f"Error getting metadata: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving system metadata",
        )
