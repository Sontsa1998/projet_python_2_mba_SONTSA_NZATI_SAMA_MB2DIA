"""Routes de l'API des clients.

Ce module définit tous les points de terminaison (endpoints) de l'API pour les opérations
sur les clients, y compris la récupération de tous les clients, les détails des clients
et l'identification des meilleurs clients.

Fonctions
---------
get_service()
    Obtenir une instance du service client.
get_all_customers(page, limit)
    Récupérer tous les clients avec pagination.
get_customer_details(customer_id)
    Récupérer les détails d'un client spécifique.
get_top_customers(n)
    Récupérer les n meilleurs clients.
"""

from fastapi import (
    APIRouter,
    HTTPException,
    Query,
    status,
)

from transaction_api import app_context
from transaction_api.logging_config import get_logger
from transaction_api.models import (
    Customer,
    CustomerSummary,
    PaginatedResponse,
    TopCustomer,
)
from transaction_api.services.customer_service import CustomerService

logger = get_logger(__name__)

router: APIRouter = APIRouter(prefix="/api/customers", tags=["customers"])


def get_service() -> CustomerService:
    """Obtenir une instance du service client.
    
    Retours
    -------
    CustomerService
        Instance du service client.
    
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
    return CustomerService(app_context.repository)


@router.get("", response_model=PaginatedResponse[CustomerSummary])
async def get_all_customers(
    page: int = Query(1, ge=1),
    limit: int = Query(50, ge=1, le=1000),
) -> PaginatedResponse[CustomerSummary]:
    """Récupérer tous les clients avec pagination.
    
    Paramètres
    ----------
    page : int
        Numéro de page (indexé à partir de 1).
    limit : int
        Nombre d'éléments par page.
    
    Retours
    -------
    PaginatedResponse[CustomerSummary]
        Réponse paginée contenant les résumés des clients.
    
    Lève
    ----
    HTTPException
        En cas d'erreur lors de la récupération.
    """
    try:
        service = get_service()
        return service.get_all_customers(page=page, limit=limit)
    except Exception as e:
        logger.error(f"Error getting customers: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving customers",
        )


@router.get("/{customer_id}", response_model=Customer)
async def get_customer_details(customer_id: str) -> Customer:
    """Récupérer les détails d'un client spécifique.
    
    Paramètres
    ----------
    customer_id : str
        L'identifiant unique du client.
    
    Retours
    -------
    Customer
        Objet contenant les détails du client.
    
    Lève
    ----
    HTTPException
        En cas d'erreur lors de la récupération.
    """
    try:
        service = get_service()
        return service.get_customer_details(customer_id)
    except Exception as e:
        logger.error(f"Error getting customer details: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving customer details",
        )


@router.get("/Ranked/top", response_model=list[TopCustomer])
async def get_top_customers(
    n: int = Query(
        10,
        ge=1,
        le=1000,
        description="Number of top customers",
    ),
) -> list[TopCustomer]:
    """Récupérer les n meilleurs clients par nombre de transactions.
    
    Paramètres
    ----------
    n : int
        Nombre de meilleurs clients à retourner.
    
    Retours
    -------
    list[TopCustomer]
        Liste des n meilleurs clients.
    
    Lève
    ----
    HTTPException
        En cas d'erreur lors de la récupération.
    """
    try:
        service = get_service()
        return service.get_top_customers(n=n)
    except Exception as e:
        logger.error(f"Error getting top customers: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving top customers",
        )
