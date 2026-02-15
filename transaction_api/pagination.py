"""Utilitaires de pagination pour l'API Transaction.

Ce module fournit des utilitaires pour gérer la pagination dans les réponses de l'API,
y compris la validation des paramètres et la création de réponses paginées.

Classes
-------
PaginationService
    Service pour gérer les opérations de pagination.

Fonctions
---------
validate_pagination_params(page, limit)
    Valider les paramètres de pagination.
create_paginated_response(data, page, limit, total_count)
    Créer une réponse paginée avec les métadonnées.
"""

from typing import Generic, List, TypeVar

from transaction_api.config import MAX_LIMIT, MIN_LIMIT
from transaction_api.exceptions import InvalidPaginationParameters
from transaction_api.models import PaginatedResponse, PaginationMetadata

T = TypeVar("T")


class PaginationService(Generic[T]):
    """Service de gestion de la pagination.
    
    Fournit des méthodes statiques pour valider les paramètres de pagination et créer
    des réponses paginées avec les métadonnées appropriées.
    """

    @staticmethod
    def validate_pagination_params(page: int, limit: int) -> tuple[int, int]:
        """Valider les paramètres de pagination.
        
        Valide que les paramètres page et limit sont dans les plages acceptables
        telles que définies dans la configuration.
        
        Paramètres
        ----------
        page : int
            Le numéro de page (indexé à partir de 1).
        limit : int
            Le nombre d'éléments par page.
        
        Retours
        -------
        tuple[int, int]
            Tuple de (page, limit) si la validation réussit.
        
        Lève
        ----
        InvalidPaginationParameters
            Si page est inférieur à 1 ou limit est en dehors de la plage autorisée.
        
        Exemples
        --------
        >>> page, limit = PaginationService.validate_pagination_params(1, 50)
        >>> page, limit
        (1, 50)
        """
        if page < 1:
            raise InvalidPaginationParameters("Page must be >= 1")
        if limit < MIN_LIMIT or limit > MAX_LIMIT:
            raise InvalidPaginationParameters(
                f"Limit must be between {MIN_LIMIT} and {MAX_LIMIT}"
            )
        return page, limit

    @staticmethod
    def create_paginated_response(
        data: List[T], page: int, limit: int, total_count: int
    ) -> PaginatedResponse[T]:
        """Créer une réponse paginée.
        
        Crée un objet de réponse paginée avec les données fournies et les
        métadonnées de pagination calculées automatiquement.
        
        Paramètres
        ----------
        data : List[T]
            Liste d'éléments pour la page actuelle.
        page : int
            Numéro de page actuel (indexé à partir de 1).
        limit : int
            Nombre d'éléments par page.
        total_count : int
            Nombre total d'éléments sur toutes les pages.
        
        Retours
        -------
        PaginatedResponse[T]
            Réponse paginée avec les données et les métadonnées de pagination.
        
        Exemples
        --------
        >>> items = [item1, item2, item3]
        >>> response = PaginationService.create_paginated_response(
        ...     items, page=1, limit=50, total_count=100
        ... )
        >>> response.pagination.has_next_page
        True
        """
        total_pages = (total_count + limit - 1) // limit
        has_next_page = page < total_pages

        pagination_metadata = PaginationMetadata(
            page=page,
            limit=limit,
            total_count=total_count,
            total_pages=total_pages,
            has_next_page=has_next_page,
        )

        return PaginatedResponse(data=data, pagination=pagination_metadata)
