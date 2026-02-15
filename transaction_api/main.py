"""Application FastAPI principale.

Ce module configure l'application FastAPI avec toutes les routes, les gestionnaires
d'exceptions et la gestion du cycle de vie pour l'API Transaction.

Fonctions
---------
lifespan(app)
    Gestionnaire de contexte asynchrone pour le démarrage et l'arrêt de l'application.
transaction_not_found_handler(request, exc)
    Gestionnaire d'exception pour les erreurs TransactionNotFound.
customer_not_found_handler(request, exc)
    Gestionnaire d'exception pour les erreurs CustomerNotFound.
invalid_pagination_handler(request, exc)
    Gestionnaire d'exception pour les erreurs InvalidPaginationParameters.
invalid_search_filters_handler(request, exc)
    Gestionnaire d'exception pour les erreurs InvalidSearchFilters.
general_exception_handler(request, exc)
    Gestionnaire d'exception pour les exceptions générales.
health_check()
    Point de terminaison de vérification de santé.
"""

from contextlib import asynccontextmanager
from datetime import datetime

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from transaction_api import app_context
from transaction_api.config import API_DESCRIPTION, API_TITLE, API_VERSION
from transaction_api.exceptions import (
    CustomerNotFound,
    InvalidPaginationParameters,
    InvalidSearchFilters,
    TransactionNotFound,
)
from transaction_api.logging_config import get_logger, setup_logging
from transaction_api.repository import TransactionRepository
from transaction_api.routes import (
    transaction_routes as transaction_routes_mod,
    statistics_routes as statistics_routes_mod,
    fraud_routes as fraud_routes_mod,
    customer_routes as customer_routes_mod,
    system_routes as system_routes_mod,
)

transaction_router = transaction_routes_mod.router
statistics_router = statistics_routes_mod.router
fraud_router = fraud_routes_mod.router
customer_router = customer_routes_mod.router
system_router = system_routes_mod.router

# Set up logging
setup_logging()
logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gestionnaire de contexte de cycle de vie pour l'application FastAPI.
    
    Gère les événements de démarrage et d'arrêt de l'application. Initialise le
    référentiel de transaction et charge les données du CSV au démarrage.
    
    Paramètres
    ----------
    app : FastAPI
        L'instance de l'application FastAPI.
    
    Cède
    ----
    None
    
    Lève
    ----
    Exception
        Si le chargement des données de transaction échoue.
    """
    logger.info("Starting Transaction API")
    app_context.repository = TransactionRepository()
    try:
        logger.info("Loading transaction data from CSV")
        app_context.repository.load_from_csv()
        total_transactions = len(app_context.repository.get_all_transactions())
        logger.info(f"Successfully loaded {total_transactions} transactions")
    except Exception as e:
        logger.error(f"Failed to load transaction data: {e}")
        raise
    yield
    logger.info("Shutting down Transaction API")


# Create FastAPI app
app = FastAPI(
    title=API_TITLE,
    description=API_DESCRIPTION,
    version=API_VERSION,
    lifespan=lifespan,
)


@app.exception_handler(TransactionNotFound)
async def transaction_not_found_handler(
    request: Request, exc: TransactionNotFound
):
    """Gérer l'exception TransactionNotFound.
    
    Retourne une réponse 404 quand une transaction demandée n'est pas trouvée.
    
    Paramètres
    ----------
    request : Request
        L'objet de requête HTTP.
    exc : TransactionNotFound
        L'exception qui a été levée.
    
    Retours
    -------
    JSONResponse
        Réponse JSON avec les détails d'erreur et le code de statut 404.
    """
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            "error": "Transaction not found",
            "details": str(exc),
            "timestamp": datetime.utcnow().isoformat(),
        },
    )


@app.exception_handler(CustomerNotFound)
async def customer_not_found_handler(request: Request, exc: CustomerNotFound):
    """Gérer l'exception CustomerNotFound.
    
    Retourne une réponse 404 quand un client demandé n'est pas trouvé.
    
    Paramètres
    ----------
    request : Request
        L'objet de requête HTTP.
    exc : CustomerNotFound
        L'exception qui a été levée.
    
    Retours
    -------
    JSONResponse
        Réponse JSON avec les détails d'erreur et le code de statut 404.
    """
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            "error": "Customer not found",
            "details": str(exc),
            "timestamp": datetime.utcnow().isoformat(),
        },
    )


@app.exception_handler(InvalidPaginationParameters)
async def invalid_pagination_handler(
    request: Request,
    exc: InvalidPaginationParameters,
):
    """Gérer l'exception InvalidPaginationParameters.
    
    Retourne une réponse 400 quand les paramètres de pagination sont invalides.
    
    Paramètres
    ----------
    request : Request
        L'objet de requête HTTP.
    exc : InvalidPaginationParameters
        L'exception qui a été levée.
    
    Retours
    -------
    JSONResponse
        Réponse JSON avec les détails d'erreur et le code de statut 400.
    """
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "error": "Invalid pagination parameters",
            "details": str(exc),
            "timestamp": datetime.utcnow().isoformat(),
        },
    )


@app.exception_handler(InvalidSearchFilters)
async def invalid_search_filters_handler(
    request: Request, exc: InvalidSearchFilters
):
    """Gérer l'exception InvalidSearchFilters.
    
    Retourne une réponse 400 quand les filtres de recherche sont invalides.
    
    Paramètres
    ----------
    request : Request
        L'objet de requête HTTP.
    exc : InvalidSearchFilters
        L'exception qui a été levée.
    
    Retours
    -------
    JSONResponse
        Réponse JSON avec les détails d'erreur et le code de statut 400.
    """
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "error": "Invalid search filters",
            "details": str(exc),
            "timestamp": datetime.utcnow().isoformat(),
        },
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Gérer les exceptions générales.
    
    Capture toute exception non gérée et retourne une réponse d'erreur 500.
    
    Paramètres
    ----------
    request : Request
        L'objet de requête HTTP.
    exc : Exception
        L'exception qui a été levée.
    
    Retours
    -------
    JSONResponse
        Réponse JSON avec les détails d'erreur et le code de statut 500.
    """
    logger.error(f"Unexpected error: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Internal server error",
            "details": "An unexpected error occurred",
            "timestamp": datetime.utcnow().isoformat(),
        },
    )


@app.get("/health")
async def health_check():
    """Point de terminaison de vérification de santé.
    
    Retourne l'état de santé de l'API.
    
    Retours
    -------
    dict
        Dictionnaire avec l'indicateur d'état.
    
    Exemples
    --------
    >>> response = await health_check()
    >>> response["status"]
    'ok'
    """
    return {"status": "ok"}


# Include routers
app.include_router(transaction_router)
app.include_router(statistics_router)
app.include_router(fraud_router)
app.include_router(customer_router)
app.include_router(system_router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)