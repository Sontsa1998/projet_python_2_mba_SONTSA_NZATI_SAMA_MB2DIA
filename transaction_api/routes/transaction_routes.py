"""Routes de l'API des transactions.

Ce module définit tous les points de terminaison (endpoints) de l'API pour les opérations
sur les transactions, y compris la récupération, la recherche, la suppression et l'analyse
des transactions.

Fonctions
---------
get_service()
    Obtenir une instance du service de transactions.
get_all_transactions(page, limit)
    Récupérer toutes les transactions avec pagination.
get_transaction(transaction_id)
    Récupérer une transaction par son identifiant.
delete_transaction(transaction_id)
    Supprimer une transaction.
search_transactions(filters, page, limit)
    Rechercher des transactions avec des filtres.
get_transaction_types()
    Récupérer tous les types de transactions.
get_recent_transactions(limit)
    Récupérer les transactions récentes.
get_customer_transactions(customer_id, page, limit)
    Récupérer les transactions d'un client.
get_merchant_transactions(customer_id, page, limit)
    Récupérer les transactions d'un commerçant.
"""

from fastapi import (
    APIRouter,
    HTTPException,
    Query,
    status,
)

from transaction_api import app_context
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

from transaction_api.services.transaction_service import TransactionService

logger = get_logger(__name__)

router: APIRouter = APIRouter(prefix="/api/transaction", tags=["transactions"])


def get_service() -> TransactionService:
    """Obtenir une instance du service de transactions.
    
    Retours
    -------
    TransactionService
        Instance du service de transactions.
    
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
    return TransactionService(app_context.repository)

@router.get("", response_model=PaginatedResponse[Transaction])
async def get_all_transactions(
    page: int = Query(1, ge=1),
    limit: int = Query(50, ge=1, le=1000),
) -> PaginatedResponse[Transaction]:
    """Récupérer toutes les transactions avec pagination.
    
    Paramètres
    ----------
    page : int
        Numéro de page (indexé à partir de 1).
    limit : int
        Nombre d'éléments par page.
    
    Retours
    -------
    PaginatedResponse[Transaction]
        Réponse paginée contenant les transactions.
    
    Lève
    ----
    HTTPException
        En cas d'erreur lors de la récupération des transactions.
    """
    try:
        service = get_service()
        return service.get_all_transactions(page=page, limit=limit)
    except InvalidPaginationParameters as e:
        logger.error(f"Invalid pagination parameters: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    except Exception as e:
        logger.error(f"Error getting transactions: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving transactions",
        )


@router.get("/{transaction_id}", response_model=Transaction)
async def get_transaction(transaction_id: str) -> Transaction:
    """Récupérer une transaction par son identifiant.
    
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
    HTTPException
        Si la transaction n'existe pas ou en cas d'erreur.
    """
    try:
        service = get_service()
        return service.get_transaction_by_id(transaction_id)
    except TransactionNotFound as e:
        logger.warning(f"Transaction not found: {transaction_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
    except Exception as e:
        logger.error(f"Error getting transaction: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving transaction",
        )

@router.delete("/{transaction_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_transaction(transaction_id: str) -> None:
    """Supprimer une transaction.
    
    Paramètres
    ----------
    transaction_id : str
        L'identifiant unique de la transaction à supprimer.
    
    Lève
    ----
    HTTPException
        Si la transaction n'existe pas ou en cas d'erreur.
    """
    try:
        service = get_service()
        service.delete_transaction(transaction_id)
    except TransactionNotFound as e:
        logger.warning(f"Transaction not found for deletion: {transaction_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
    except Exception as e:
        logger.error(f"Error deleting transaction: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error deleting transaction",
        )


@router.post(
    "/transactionResearch/search",
    response_model=PaginatedResponse[Transaction],
)
async def search_transactions(
    filters: SearchFilters,
    page: int = Query(1, ge=1),
    limit: int = Query(50, ge=1, le=1000),
) -> PaginatedResponse[Transaction]:
    """Rechercher des transactions avec des filtres multi-critères.
    
    Paramètres
    ----------
    filters : SearchFilters
        Critères de filtrage pour la recherche.
    page : int
        Numéro de page (indexé à partir de 1).
    limit : int
        Nombre d'éléments par page.
    
    Retours
    -------
    PaginatedResponse[Transaction]
        Réponse paginée contenant les transactions filtrées.
    
    Lève
    ----
    HTTPException
        En cas d'erreur lors de la recherche.
    """
    try:
        service = get_service()
        return service.search_transactions(
            filters=filters, page=page, limit=limit
        )
    except InvalidPaginationParameters as e:
        logger.error(f"Invalid pagination parameters: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    except Exception as e:
        logger.error(f"Error searching transactions: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error searching transactions",
        )

@router.get(
    "/Type/types",
    response_model=list[dict],
)
async def get_transaction_types() -> list[dict]:
    """Récupérer tous les types de transactions avec les comptages.
    
    Retours
    -------
    list[dict]
        Liste des types de transactions avec leurs comptages.
    
    Lève
    ----
    HTTPException
        En cas d'erreur lors de la récupération.
    """
    try:
        service = get_service()
        return service.get_transaction_types()
    except Exception as e:
        logger.error(f"Error getting transaction types: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving transaction types",
        )

@router.get(
    "/Latest/recent",
    response_model=PaginatedResponse[Transaction],
)
async def get_recent_transactions(
    limit: int = Query(50, ge=1, le=1000),
) -> PaginatedResponse[Transaction]:
    """Récupérer les transactions récentes.
    
    Paramètres
    ----------
    limit : int
        Nombre maximum de transactions à retourner.
    
    Retours
    -------
    PaginatedResponse[Transaction]
        Réponse paginée contenant les transactions récentes.
    
    Lève
    ----
    HTTPException
        En cas d'erreur lors de la récupération.
    """
    try:
        service = get_service()
        return service.get_recent_transactions(limit=limit)
    except InvalidPaginationParameters as e:
        logger.error(f"Invalid limit: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    except Exception as e:
        logger.error(f"Error getting recent transactions: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving recent transactions",
        )

@router.get(
    "/by-customer/{customer_id}",
    response_model=PaginatedResponse[Transaction],
)
async def get_customer_transactions(
    customer_id: str,
    page: int = Query(1, ge=1),
    limit: int = Query(50, ge=1, le=1000),
) -> PaginatedResponse[Transaction]:
    """Récupérer les transactions d'un client.
    
    Paramètres
    ----------
    customer_id : str
        L'identifiant unique du client.
    page : int
        Numéro de page (indexé à partir de 1).
    limit : int
        Nombre d'éléments par page.
    
    Retours
    -------
    PaginatedResponse[Transaction]
        Réponse paginée contenant les transactions du client.
    
    Lève
    ----
    HTTPException
        En cas d'erreur lors de la récupération.
    """
    try:
        service = get_service()
        return service.get_customer_transactions(
            customer_id=customer_id, page=page, limit=limit
        )
    except InvalidPaginationParameters as e:
        logger.error(f"Invalid pagination parameters: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    except Exception as e:
        logger.error(f"Error getting customer transactions: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving customer transactions",
        )

@router.get(
    "/to-customer/{customer_id}",
    response_model=PaginatedResponse[Transaction],
)
async def get_merchant_transactions(
    customer_id: str,
    page: int = Query(1, ge=1),
    limit: int = Query(50, ge=1, le=1000),
) -> PaginatedResponse[Transaction]:
    """Récupérer les transactions d'un commerçant.
    
    Paramètres
    ----------
    customer_id : str
        L'identifiant unique du commerçant.
    page : int
        Numéro de page (indexé à partir de 1).
    limit : int
        Nombre d'éléments par page.
    
    Retours
    -------
    PaginatedResponse[Transaction]
        Réponse paginée contenant les transactions du commerçant.
    
    Lève
    ----
    HTTPException
        En cas d'erreur lors de la récupération.
    """
    try:
        service = get_service()
        return service.get_merchant_transactions(
            merchant_id=customer_id, page=page, limit=limit
        )
    except InvalidPaginationParameters as e:
        logger.error(f"Invalid pagination parameters: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    except Exception as e:
        logger.error(f"Error getting merchant transactions: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving merchant transactions",
        )
