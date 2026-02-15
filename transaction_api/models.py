"""Modèles Pydantic pour l'API Transaction.

Ce module définit tous les modèles de données Pydantic utilisés dans l'API Transaction,
y compris les données de transaction, les métadonnées de pagination, les statistiques,
la détection de fraude et les informations sur les clients.

Classes
-------
Transaction
    Représente un enregistrement de transaction unique avec tous les détails associés.
PaginationMetadata
    Contient les informations de pagination pour les réponses paginées.
PaginatedResponse
    Wrapper de réponse paginée générique pour tout type de données.
OverviewStats
    Statistiques générales pour toutes les transactions.
AmountBucket
    Représente un bucket dans l'analyse de distribution des montants.
AmountDistribution
    Statistiques de distribution des montants par buckets.
TypeStats
    Statistiques pour un type de transaction spécifique.
DailyStats
    Statistiques quotidiennes des transactions.
FraudSummary
    Résumé des résultats de détection de fraude.
FraudTypeStats
    Statistiques de fraude ventilées par type de transaction.
FraudUseChipStats
    Statistiques de fraude ventilées par type use_chip.
FraudPrediction
    Résultat de la prédiction de fraude pour une transaction.
Customer
    Détails du client et résumé des transactions.
TopCustomer
    Résumé d'un client principal par volume de transactions.
CustomerSummary
    Informations de résumé client de base.
HealthStatus
    Informations d'état de santé du système.
SystemMetadata
    Métadonnées du système et statistiques.
ErrorResponse
    Format de réponse d'erreur standard.
SearchFilters
    Paramètres de filtre de recherche pour les requêtes de transactions.
"""

from datetime import date as date_type
from datetime import datetime
from typing import Generic, List, Optional, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


class Transaction(BaseModel):
    """Modèle de données de transaction.
    
    Représente un enregistrement de transaction unique avec tous les détails associés,
    y compris la date, les informations du client, les détails de la carte, les
    informations du commerçant et le montant.
    
    Attributs
    ---------
    id : str
        Identifiant unique de la transaction.
    date : datetime
        Date et heure d'occurrence de la transaction.
    client_id : str
        Identifiant du client/consommateur effectuant la transaction.
    card_id : str
        Identifiant de la carte utilisée pour la transaction.
    amount : float
        Montant de la transaction en unités monétaires.
    use_chip : str
        Type de transaction (ex: "Swipe Transaction", "Chip Transaction").
    merchant_id : str
        Identifiant du commerçant où la transaction a eu lieu.
    merchant_city : str
        Ville où le commerçant est situé.
    merchant_state : str
        État/province où le commerçant est situé.
    zip : str
        Code postal du lieu du commerçant.
    mcc : str
        Code de catégorie de commerçant pour la classification.
    errors : str, optionnel
        Indicateur d'erreur signalant si la transaction a des erreurs.
    
    Exemples
    --------
    >>> transaction = Transaction(
    ...     id="1",
    ...     date=datetime(2023, 1, 1, 12, 0, 0),
    ...     client_id="C001",
    ...     card_id="CARD001",
    ...     amount=100.50,
    ...     use_chip="Swipe Transaction",
    ...     merchant_id="M001",
    ...     merchant_city="New York",
    ...     merchant_state="NY",
    ...     zip="10001",
    ...     mcc="5411",
    ...     errors=None
    ... )
    """

    id: str = Field(..., description="Transaction id")
    date: datetime = Field(..., description="Transaction date and time")
    client_id: str = Field(..., description="Client id")
    card_id: str = Field(..., description="Card id")
    amount: float = Field(..., description="Amount")
    use_chip: str = Field(..., description="Transaction type")
    merchant_id: str = Field(..., description="Merchant id")
    merchant_city: str = Field(..., description="Merchant city")
    merchant_state: str = Field(..., description="Merchant state")
    zip: str = Field(..., description="ZIP code")
    mcc: str = Field(..., description="Merchant category code")
    errors: Optional[str] = Field(None, description="Error flag")

    class Config:
        """Configuration Pydantic pour le modèle Transaction.
        
        Fournit un exemple de schéma JSON pour la documentation de l'API.
        """

        json_schema_extra = {
            "example": {
                "id": "1",
                "date": "2023-01-01T12:00:00",
                "client_id": "C001",
                "card_id": "CARD001",
                "amount": 100.50,
                "use_chip": "Swipe Transaction",
                "merchant_id": "M001",
                "merchant_city": "New York",
                "merchant_state": "NY",
                "zip": "10001",
                "mcc": "5411",
                "errors": None,
            }
        }


class PaginationMetadata(BaseModel):
    """Métadonnées de pagination.
    
    Contient les informations sur l'état de la pagination, y compris la page actuelle,
    la limite, les totaux et les indicateurs de navigation.
    
    Attributs
    ---------
    page : int
        Numéro de page actuel (indexé à partir de 1).
    limit : int
        Nombre d'éléments par page.
    total_count : int
        Nombre total d'éléments sur toutes les pages.
    total_pages : int
        Nombre total de pages disponibles.
    has_next_page : bool
        Indique s'il y a une page suivante disponible.
    """

    page: int = Field(..., description="Current page number")
    limit: int = Field(..., description="Items per page")
    total_count: int = Field(..., description="Total items")
    total_pages: int = Field(..., description="Total pages")
    has_next_page: bool = Field(..., description="Has next page")


class PaginatedResponse(BaseModel, Generic[T]):
    """Réponse paginée générique.
    
    Enveloppe une liste d'éléments avec les métadonnées de pagination pour les
    réponses API paginées.
    
    Attributs
    ---------
    data : List[T]
        Liste d'éléments pour la page actuelle.
    pagination : PaginationMetadata
        Informations de pagination et détails de navigation.
    
    Exemples
    --------
    >>> response = PaginatedResponse(
    ...     data=[item1, item2],
    ...     pagination=PaginationMetadata(
    ...         page=1, limit=50, total_count=100,
    ...         total_pages=2, has_next_page=True
    ...     )
    ... )
    """

    data: List[T] = Field(..., description="List of items")
    pagination: PaginationMetadata = Field(..., description="Pagination info")


class OverviewStats(BaseModel):
    """Statistiques d'aperçu.
    
    Fournit des statistiques de haut niveau sur toutes les transactions du système.
    
    Attributs
    ---------
    total_count : int
        Nombre total de transactions.
    total_amount : float
        Somme de tous les montants de transaction.
    average_amount : float
        Montant moyen de transaction.
    min_date : datetime
        Date de transaction la plus ancienne.
    max_date : datetime
        Date de transaction la plus récente.
    """

    total_count: int = Field(..., description="Total transactions")
    total_amount: float = Field(..., description="Total amount")
    average_amount: float = Field(..., description="Average amount")
    min_date: datetime = Field(..., description="Earliest date")
    max_date: datetime = Field(..., description="Latest date")


class AmountBucket(BaseModel):
    """Bucket de distribution des montants.
    
    Représente un seul bucket dans l'analyse de distribution des montants.
    
    Attributs
    ---------
    range : str
        Étiquette décrivant la plage de montants (ex: "0-100").
    count : int
        Nombre de transactions dans ce bucket.
    percentage : float
        Pourcentage du total des transactions dans ce bucket.
    """

    range: str = Field(..., description="Range label")
    count: int = Field(..., description="Bucket count")
    percentage: float = Field(..., description="Percentage of total")


class AmountDistribution(BaseModel):
    """Statistiques de distribution des montants.
    
    Contient la distribution des transactions sur les buckets de montants.
    
    Attributs
    ---------
    buckets : List[AmountBucket]
        Liste des buckets de distribution des montants.
    """

    buckets: List[AmountBucket] = Field(..., description="Buckets")


class TypeStats(BaseModel):
    """Statistiques pour un type de transaction.
    
    Fournit des statistiques pour un type de transaction spécifique.
    
    Attributs
    ---------
    type : str
        Identifiant du type de transaction.
    count : int
        Nombre de transactions de ce type.
    total_amount : float
        Somme des montants pour ce type de transaction.
    average_amount : float
        Montant moyen pour ce type de transaction.
    """

    type: str = Field(..., description="Transaction type")
    count: int = Field(..., description="Count")
    total_amount: float = Field(..., description="Total amount")
    average_amount: float = Field(..., description="Average amount")


class DailyStats(BaseModel):
    """Statistiques quotidiennes.
    
    Fournit les statistiques de transaction pour un jour spécifique.
    
    Attributs
    ---------
    date : date_type
        La date pour ces statistiques.
    count : int
        Nombre de transactions à cette date.
    total_amount : float
        Somme des montants de transaction à cette date.
    average_amount : float
        Montant moyen de transaction à cette date.
    """

    date: date_type = Field(..., description="Date")
    count: int = Field(..., description="Count")
    total_amount: float = Field(..., description="Total amount")
    average_amount: float = Field(..., description="Average amount")


class FraudSummary(BaseModel):
    """Résumé de détection de fraude.
    
    Fournit les statistiques globales de détection de fraude.
    
    Attributs
    ---------
    total_fraud_count : int
        Nombre total de transactions frauduleuses détectées.
    fraud_rate : float
        Pourcentage de transactions signalées comme frauduleuses.
    total_fraud_amount : float
        Somme des montants dans les transactions frauduleuses.
    """

    total_fraud_count: int = Field(..., description="Fraud count")
    fraud_rate: float = Field(..., description="Fraud rate")
    total_fraud_amount: float = Field(..., description="Fraud amount")


class FraudTypeStats(BaseModel):
    """Statistiques de fraude par type.
    
    Fournit les statistiques de fraude ventilées par type de transaction.
    
    Attributs
    ---------
    type : str
        Identifiant du type de transaction.
    fraud_count : int
        Nombre de transactions frauduleuses de ce type.
    fraud_rate : float
        Taux de fraude pour ce type de transaction.
    total_count : int
        Total des transactions de ce type.
    """

    type: str = Field(..., description="Transaction type")
    fraud_count: int = Field(..., description="Fraud count")
    fraud_rate: float = Field(..., description="Fraud rate")
    total_count: int = Field(..., description="Total count")


class FraudUseChipStats(BaseModel):
    """Statistiques de fraude par type use_chip.
    
    Fournit les statistiques de fraude ventilées par type use_chip.
    
    Attributs
    ---------
    use_chip : str
        Identifiant du type use_chip.
    fraud_count : int
        Nombre de transactions frauduleuses de ce type use_chip.
    fraud_rate : float
        Taux de fraude pour ce type use_chip.
    total_count : int
        Total des transactions de ce type use_chip.
    """

    use_chip: str = Field(..., description="use_chip type")
    fraud_count: int = Field(..., description="Fraud count")
    fraud_rate: float = Field(..., description="Fraud rate")
    total_count: int = Field(..., description="Total count")


class FraudPrediction(BaseModel):
    """Résultat de prédiction de fraude.
    
    Contient le résultat de la prédiction de fraude pour une transaction.
    
    Attributs
    ---------
    fraud_score : float
        Score de probabilité de fraude entre 0.0 et 1.0.
    reasoning : str
        Explication de la prédiction de fraude.
    """

    fraud_score: float = Field(..., ge=0.0, le=1.0, description="Fraud score")
    reasoning: str = Field(..., description="Reasoning")


class Customer(BaseModel):
    """Détails du client.
    
    Fournit des informations détaillées sur un client et ses transactions.
    
    Attributs
    ---------
    customer_id : str
        Identifiant unique du client.
    transaction_count : int
        Nombre total de transactions par ce client.
    total_amount : float
        Somme de tous les montants de transaction par ce client.
    average_amount : float
        Montant moyen de transaction pour ce client.
    """

    customer_id: str = Field(..., description="Customer id")
    transaction_count: int = Field(..., description="Transaction count")
    total_amount: float = Field(..., description="Total amount")
    average_amount: float = Field(..., description="Average amount")


class TopCustomer(BaseModel):
    """Résumé du client principal.
    
    Informations de résumé pour un client principal par volume de transactions.
    
    Attributs
    ---------
    customer_id : str
        Identifiant unique du client.
    transaction_count : int
        Nombre de transactions par ce client.
    total_amount : float
        Somme des montants de transaction par ce client.
    """

    customer_id: str = Field(..., description="Customer id")
    transaction_count: int = Field(..., description="Transaction count")
    total_amount: float = Field(..., description="Total transaction amount")


class CustomerSummary(BaseModel):
    """Résumé du client.
    
    Informations de résumé de base pour un client.
    
    Attributs
    ---------
    customer_id : str
        Identifiant unique du client.
    transaction_count : int
        Nombre de transactions par ce client.
    """

    customer_id: str = Field(..., description="Customer id")
    transaction_count: int = Field(..., description="Transaction count")


class HealthStatus(BaseModel):
    """État de santé du système.
    
    Indique l'état de santé actuel du système.
    
    Attributs
    ---------
    status : str
        Indicateur d'état de santé (ex: "healthy", "degraded").
    response_time_ms : float
        Temps de réponse en millisecondes.
    """

    status: str = Field(..., description="Health status")
    response_time_ms: float = Field(..., description="Response time ms")


class SystemMetadata(BaseModel):
    """Métadonnées du système.
    
    Contient les métadonnées et statistiques à l'échelle du système.
    
    Attributs
    ---------
    total_transaction_count : int
        Nombre total de transactions dans le système.
    data_load_date : datetime
        Quand les données de transaction ont été chargées.
    api_version : str
        Version actuelle de l'API.
    min_date : datetime
        Date de transaction la plus ancienne du système.
    max_date : datetime
        Date de transaction la plus récente du système.
    """

    total_transaction_count: int = Field(..., description="Total transactions")
    data_load_date: datetime = Field(..., description="Data load date")
    api_version: str = Field(..., description="API version")
    min_date: datetime = Field(..., description="Earliest date")
    max_date: datetime = Field(..., description="Latest date")


class ErrorResponse(BaseModel):
    """Réponse d'erreur.
    
    Format standard pour les réponses d'erreur de l'API.
    
    Attributs
    ---------
    error : str
        Message d'erreur.
    details : str, optionnel
        Détails d'erreur supplémentaires.
    timestamp : datetime
        Quand l'erreur s'est produite.
    """

    error: str = Field(..., description="Error message")
    details: Optional[str] = Field(None, description="Details")
    timestamp: datetime = Field(..., description="Timestamp")


class SearchFilters(BaseModel):
    """Filtres de recherche pour les transactions.
    
    Définit les filtres optionnels pour les requêtes de recherche de transactions.
    
    Attributs
    ---------
    min_amount : float, optionnel
        Filtre de montant minimum de transaction.
    max_amount : float, optionnel
        Filtre de montant maximum de transaction.
    client_id : str, optionnel
        Filtrer par ID client/consommateur.
    transaction_id : str, optionnel
        Filtrer par ID de transaction.
    merchant_city : str, optionnel
        Filtrer par ville du commerçant.
    use_chip : str, optionnel
        Filtrer par type de transaction.
    """

    min_amount: Optional[float] = Field(None, description="Min amount")
    max_amount: Optional[float] = Field(None, description="Max amount")
    client_id: Optional[str] = Field(None, description="Client id")
    transaction_id: Optional[str] = Field(None, description="Transaction id")
    merchant_city: Optional[str] = Field(None, description="Merchant city")
    use_chip: Optional[str] = Field(None, description="Transaction type")
