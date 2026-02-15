"""Service de santé et de métadonnées pour la logique métier.

Ce module fournit la classe HealthService qui gère les vérifications de santé
du système et la récupération des métadonnées du système.

Classes
-------
HealthService
    Service pour les vérifications de santé et les métadonnées.
"""

import time
from datetime import datetime

from transaction_api.config import API_VERSION
from transaction_api.logging_config import get_logger
from transaction_api.models import HealthStatus, SystemMetadata
from transaction_api.repository import TransactionRepository

logger = get_logger(__name__)


class HealthService:
    """Service pour les vérifications de santé et les métadonnées.
    
    Gère les vérifications de santé du système et la récupération des métadonnées
    du système, y compris les informations de version et les statistiques de données.
    
    Attributs
    ---------
    repository : TransactionRepository
        Le référentiel de transactions utilisé pour accéder aux données.
    """

    def __init__(self, repository: TransactionRepository) -> None:
        """Initialiser le service.
        
        Paramètres
        ----------
        repository : TransactionRepository
            Le référentiel de transactions pour accéder aux données.
        """
        self.repository = repository

    def check_health(self) -> HealthStatus:
        """Vérifier la santé du système.
        
        Effectue une vérification de santé du système en testant l'accessibilité
        du référentiel et en mesurant le temps de réponse.
        
        Retours
        -------
        HealthStatus
            Objet contenant l'état de santé et le temps de réponse.
        
        Exemples
        --------
        >>> service = HealthService(repository)
        >>> health = service.check_health()
        >>> health.status
        'healthy'
        """
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
    
    def get_metadata(self) -> SystemMetadata:
        """Récupérer les métadonnées du système.
        
        Récupère les métadonnées du système, y compris le nombre total de transactions,
        la date de chargement des données, la version de l'API et les dates min/max.
        
        Retours
        -------
        SystemMetadata
            Objet contenant les métadonnées du système.
        
        Exemples
        --------
        >>> service = HealthService(repository)
        >>> metadata = service.get_metadata()
        >>> metadata.api_version
        '1.0.0'
        """
        transactions = self.repository.get_all_transactions()
        total_count = len(transactions)

        if transactions:
            min_date = min(t.date for t in transactions)
            max_date = max(t.date for t in transactions)
        else:
            now = datetime.utcnow()
            min_date = now
            max_date = now

        data_load_date = self.repository.data_load_date or datetime.utcnow()

        return SystemMetadata(
            total_transaction_count=total_count,
            data_load_date=data_load_date,
            api_version=API_VERSION,
            min_date=min_date,
            max_date=max_date,
        )