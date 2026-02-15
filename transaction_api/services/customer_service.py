"""Service client pour la logique métier.

Ce module fournit la classe CustomerService qui gère les opérations liées aux clients,
y compris la récupération des détails des clients, la pagination et l'identification
des clients les plus actifs.

Classes
-------
CustomerService
    Service pour les opérations sur les clients.
"""

from typing import List

from transaction_api.exceptions import InvalidPaginationParameters
from transaction_api.logging_config import get_logger
from transaction_api.models import (
    Customer,
    CustomerSummary,
    PaginatedResponse,
    TopCustomer,
)
from transaction_api.pagination import PaginationService
from transaction_api.repository import TransactionRepository

logger = get_logger(__name__)


class CustomerService:
    """Service pour les opérations sur les clients.
    
    Gère les opérations liées aux clients, y compris la récupération de tous les clients,
    les détails des clients individuels et l'identification des clients les plus actifs.
    
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

    def get_all_customers(
        self, page: int = 1, limit: int = 50
    ) -> PaginatedResponse[CustomerSummary]:
        """Récupérer tous les clients avec pagination.
        
        Récupère une liste paginée de tous les clients avec le nombre de transactions
        pour chaque client.
        
        Paramètres
        ----------
        page : int, optionnel
            Numéro de page (indexé à partir de 1). Par défaut 1.
        limit : int, optionnel
            Nombre d'éléments par page. Par défaut 50.
        
        Retours
        -------
        PaginatedResponse[CustomerSummary]
            Réponse paginée contenant les résumés des clients.
        
        Lève
        ----
        InvalidPaginationParameters
            Si les paramètres de pagination sont invalides.
        
        Exemples
        --------
        >>> service = CustomerService(repository)
        >>> response = service.get_all_customers(page=1, limit=50)
        >>> len(response.data)
        50
        """
        try:
            page, limit = PaginationService.validate_pagination_params(
                page, limit
            )
        except InvalidPaginationParameters as e:
            logger.error(f"Invalid pagination parameters: {e}")
            raise

        customer_ids = self.repository.get_all_customers()
        total_count = len(customer_ids)

        # Sort customer IDs for consistent pagination
        customer_ids = sorted(customer_ids)

        # Apply pagination
        offset = (page - 1) * limit
        paginated_ids = customer_ids[offset: offset + limit]

        # Create customer summaries
        customers = []
        for customer_id in paginated_ids:
            transaction_count = len(
                self.repository.get_by_customer(
                    customer_id, page=1, limit=1000000
                )[0]
            )
            customers.append(
                CustomerSummary(
                    customer_id=customer_id,
                    transaction_count=transaction_count,
                )
            )

        return PaginationService.create_paginated_response(
            customers, page, limit, total_count
        )

    def get_customer_details(self, customer_id: str) -> Customer:
        """Récupérer les détails d'un client spécifique.
        
        Récupère les informations détaillées d'un client, y compris le nombre total
        de transactions, le montant total et le montant moyen.
        
        Paramètres
        ----------
        customer_id : str
            L'identifiant unique du client.
        
        Retours
        -------
        Customer
            Objet contenant les détails du client.
        
        Exemples
        --------
        >>> service = CustomerService(repository)
        >>> customer = service.get_customer_details("C001")
        >>> customer.transaction_count
        42
        """
        transactions, total_count = self.repository.get_by_customer(
            customer_id, page=1, limit=1000000
        )

        if not transactions:
            # Return empty customer
            return Customer(
                customer_id=customer_id,
                transaction_count=0,
                total_amount=0.0,
                average_amount=0.0,
            )

        total_amount = sum(t.amount for t in transactions)
        average_amount = (
            total_amount / len(transactions) if transactions else 0.0
        )

        return Customer(
            customer_id=customer_id,
            transaction_count=len(transactions),
            total_amount=total_amount,
            average_amount=average_amount,
        )

    def get_top_customers(self, n: int = 10) -> List[TopCustomer]:
        """Récupérer les n meilleurs clients par nombre de transactions.
        
        Identifie et retourne les clients les plus actifs en fonction du nombre
        de transactions qu'ils ont effectuées.
        
        Paramètres
        ----------
        n : int, optionnel
            Nombre de clients à retourner. Par défaut 10.
        
        Retours
        -------
        List[TopCustomer]
            Liste des n meilleurs clients triés par nombre de transactions décroissant.
        
        Exemples
        --------
        >>> service = CustomerService(repository)
        >>> top_customers = service.get_top_customers(n=5)
        >>> len(top_customers)
        5
        >>> top_customers[0].transaction_count >= top_customers[1].transaction_count
        True
        """
        customer_ids = self.repository.get_all_customers()

        # Get customer details for all customers
        top_customers_list: List[TopCustomer] = []
        for customer_id in customer_ids:
            transactions, _ = self.repository.get_by_customer(
                customer_id, page=1, limit=1000000
            )
            if transactions:
                total_amount = sum(t.amount for t in transactions)
                top_customers_list.append(
                    TopCustomer(
                        customer_id=customer_id,
                        transaction_count=len(transactions),
                        total_amount=total_amount,
                    )
                )

        # Sort by transaction count descending
        top_customers_list.sort(
            key=lambda c: c.transaction_count,
            reverse=True,
        )

        # Get only top n customers
        return top_customers_list[:n]
