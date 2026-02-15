"""Service de transactions pour la logique métier.

Ce module fournit la classe TransactionService qui gère les opérations liées aux transactions,
y compris la récupération, la recherche, la suppression et l'analyse des transactions.

Classes
-------
TransactionService
    Service pour les opérations sur les transactions.
"""

from typing import List

from transaction_api.exceptions import (
    InvalidPaginationParameters,
    TransactionNotFound,
)
from transaction_api.logging_config import get_logger
from transaction_api.models import (
    PaginatedResponse,
    SearchFilters,
    Transaction,
)
from transaction_api.pagination import PaginationService
from transaction_api.repository import TransactionRepository

logger = get_logger(__name__)


class TransactionService:
    """Service pour les opérations sur les transactions.
    
    Gère les opérations liées aux transactions, y compris la récupération,
    la recherche avec filtres, la suppression et l'analyse des transactions.
    
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

    def get_all_transactions(
        self, page: int = 1, limit: int = 50
    ) -> PaginatedResponse[Transaction]:
        """Récupérer toutes les transactions avec pagination.
        
        Récupère une liste paginée de toutes les transactions, triées par date
        en ordre décroissant.
        
        Paramètres
        ----------
        page : int, optionnel
            Numéro de page (indexé à partir de 1). Par défaut 1.
        limit : int, optionnel
            Nombre d'éléments par page. Par défaut 50.
        
        Retours
        -------
        PaginatedResponse[Transaction]
            Réponse paginée contenant les transactions.
        
        Lève
        ----
        InvalidPaginationParameters
            Si les paramètres de pagination sont invalides.
        """
        try:
            page, limit = PaginationService.validate_pagination_params(
                page, limit
            )
        except InvalidPaginationParameters as e:
            logger.error(f"Invalid pagination parameters: {e}")
            raise

        transactions, total_count = self.repository.get_all(
            page=page, limit=limit
        )
        return PaginationService.create_paginated_response(
            transactions, page, limit, total_count
        )
    
    def get_transaction_by_id(self, transaction_id: str) -> Transaction:
        """Récupérer une transaction par son identifiant.
        
        Récupère une transaction spécifique en utilisant son identifiant unique.
        
        Paramètres
        ----------
        transaction_id : str
            L'identifiant unique de la transaction.
        
        Retours
        -------
        Transaction
            L'objet transaction demandé.
        
        Lève
        ----
        TransactionNotFound
            Si la transaction n'existe pas.
        
        Exemples
        --------
        >>> service = TransactionService(repository)
        >>> transaction = service.get_transaction_by_id("TX001")
        >>> transaction.amount
        100.50
        """
        transaction = self.repository.get_by_id(transaction_id)
        if transaction is None:
            logger.warning(f"Transaction not found: {transaction_id}")
            msg = f"Transaction with ID {transaction_id} not found"
            raise TransactionNotFound(msg)
        return transaction

    def search_transactions(
        self, filters: SearchFilters, page: int = 1, limit: int = 50
    ) -> PaginatedResponse[Transaction]:
        """Rechercher des transactions avec des filtres.
        
        Recherche les transactions en utilisant les critères de filtrage fournis
        et retourne les résultats paginés.
        
        Paramètres
        ----------
        filters : SearchFilters
            Critères de filtrage pour la recherche.
        page : int, optionnel
            Numéro de page (indexé à partir de 1). Par défaut 1.
        limit : int, optionnel
            Nombre d'éléments par page. Par défaut 50.
        
        Retours
        -------
        PaginatedResponse[Transaction]
            Réponse paginée contenant les transactions filtrées.
        
        Lève
        ----
        InvalidPaginationParameters
            Si les paramètres de pagination sont invalides.
        """
        try:
            page, limit = PaginationService.validate_pagination_params(
                page, limit
            )
        except InvalidPaginationParameters as e:
            logger.error(f"Invalid pagination parameters: {e}")
            raise
        transactions, total_count = self.repository.search(
            filters=filters, page=page, limit=limit
        )
        return PaginationService.create_paginated_response(
            transactions, page, limit, total_count
        )
    
    def delete_transaction(self, transaction_id: str) -> None:
        """Supprimer une transaction.
        
        Supprime une transaction spécifique du référentiel.
        
        Paramètres
        ----------
        transaction_id : str
            L'identifiant unique de la transaction à supprimer.
        
        Lève
        ----
        TransactionNotFound
            Si la transaction n'existe pas.
        """
        transaction = self.repository.get_by_id(transaction_id)
        if transaction is None:
            logger.warning(
                "Transaction not found for deletion: %s",
                transaction_id,
            )
            msg = f"Transaction with ID {transaction_id} not found"
            raise TransactionNotFound(msg)

        self.repository.delete(transaction_id)
        logger.info(f"Deleted transaction: {transaction_id}")

    def get_transaction_types(self) -> List[dict]:
        """Récupérer tous les types de transactions avec les comptages.
        
        Récupère tous les types de transactions (use_chip) uniques avec le nombre
        de transactions pour chaque type.
        
        Retours
        -------
        List[dict]
            Liste de dictionnaires contenant le type et le nombre de transactions.
        
        Exemples
        --------
        >>> service = TransactionService(repository)
        >>> types = service.get_transaction_types()
        >>> types[0]["type"]
        'Swipe Transaction'
        """
        use_chip_types = self.repository.get_all_use_chip_types()
        type_stats: List[dict] = []
        
        for use_chip in use_chip_types:
            transactions = self.repository.get_all_by_use_chip(use_chip)
            type_stats.append(
                {
                    "type": use_chip,
                    "count": len(transactions),
                }
            )

        # Sort by count descending
        type_stats.sort(key=lambda x: x["count"], reverse=True)  # type: ignore
        return type_stats
    
    def get_recent_transactions(
        self, limit: int = 50
    ) -> PaginatedResponse[Transaction]:
        """Récupérer les transactions récentes.
        
        Récupère les transactions les plus récentes jusqu'à la limite spécifiée.
        
        Paramètres
        ----------
        limit : int, optionnel
            Nombre maximum de transactions à retourner. Par défaut 50.
        
        Retours
        -------
        PaginatedResponse[Transaction]
            Réponse paginée contenant les transactions récentes.
        
        Lève
        ----
        InvalidPaginationParameters
            Si la limite est invalide.
        """
        try:
            _, limit = PaginationService.validate_pagination_params(1, limit)
        except InvalidPaginationParameters as e:
            logger.error(f"Invalid limit: {e}")
            raise

        transactions, total_count = self.repository.get_all(
            page=1, limit=limit
        )
        return PaginationService.create_paginated_response(
            transactions, 1, limit, total_count
        )
    
    def get_customer_transactions(
        self, customer_id: str, page: int = 1, limit: int = 50
    ) -> PaginatedResponse[Transaction]:
        """Récupérer les transactions d'un client.
        
        Récupère toutes les transactions d'un client spécifique avec pagination.
        
        Paramètres
        ----------
        customer_id : str
            L'identifiant unique du client.
        page : int, optionnel
            Numéro de page (indexé à partir de 1). Par défaut 1.
        limit : int, optionnel
            Nombre d'éléments par page. Par défaut 50.
        
        Retours
        -------
        PaginatedResponse[Transaction]
            Réponse paginée contenant les transactions du client.
        
        Lève
        ----
        InvalidPaginationParameters
            Si les paramètres de pagination sont invalides.
        """
        try:
            page, limit = PaginationService.validate_pagination_params(
                page, limit
            )
        except InvalidPaginationParameters as e:
            logger.error(f"Invalid pagination parameters: {e}")
            raise

        transactions, total_count = self.repository.get_by_customer(
            customer_id=customer_id, page=page, limit=limit
        )
        return PaginationService.create_paginated_response(
            transactions, page, limit, total_count
        )
    
    def get_merchant_transactions(
        self, merchant_id: str, page: int = 1, limit: int = 50
    ) -> PaginatedResponse[Transaction]:
        """Récupérer les transactions d'un commerçant.
        
        Récupère toutes les transactions d'un commerçant spécifique avec pagination.
        
        Paramètres
        ----------
        merchant_id : str
            L'identifiant unique du commerçant.
        page : int, optionnel
            Numéro de page (indexé à partir de 1). Par défaut 1.
        limit : int, optionnel
            Nombre d'éléments par page. Par défaut 50.
        
        Retours
        -------
        PaginatedResponse[Transaction]
            Réponse paginée contenant les transactions du commerçant.
        
        Lève
        ----
        InvalidPaginationParameters
            Si les paramètres de pagination sont invalides.
        """
        try:
            page, limit = PaginationService.validate_pagination_params(
                page, limit
            )
        except InvalidPaginationParameters as e:
            logger.error(f"Invalid pagination parameters: {e}")
            raise

        transactions, total_count = self.repository.get_by_merchant(
            merchant_id=merchant_id, page=page, limit=limit
        )
        return PaginationService.create_paginated_response(
            transactions, page, limit, total_count
        )
