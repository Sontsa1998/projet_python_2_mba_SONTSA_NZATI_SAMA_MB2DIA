"""Service de statistiques pour la logique métier.

Ce module fournit la classe StatisticsService qui gère les opérations de calcul
et d'analyse des statistiques sur les transactions.

Classes
-------
StatisticsService
    Service pour les opérations de statistiques.
"""

from collections import defaultdict
from datetime import datetime
from typing import List

from transaction_api.config import AMOUNT_BUCKETS
from transaction_api.logging_config import get_logger
from transaction_api.models import (
    AmountBucket,
    AmountDistribution,
    OverviewStats,
    TypeStats,
)
from transaction_api.repository import TransactionRepository

logger = get_logger(__name__)


class StatisticsService:
    """Service pour les opérations de statistiques.
    
    Gère le calcul et l'analyse des statistiques sur les transactions, y compris
    les statistiques générales, la distribution des montants et les statistiques
    par type de transaction.
    
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
    
    def get_overview_stats(self) -> OverviewStats:
        """Récupérer les statistiques générales.
        
        Calcule et retourne les statistiques générales sur toutes les transactions,
        y compris le nombre total, les montants et les dates.
        
        Retours
        -------
        OverviewStats
            Objet contenant les statistiques générales.
        
        Exemples
        --------
        >>> service = StatisticsService(repository)
        >>> stats = service.get_overview_stats()
        >>> stats.total_count
        1000
        """
        transactions = self.repository.get_all_transactions()

        if not transactions:
            now = datetime.utcnow()
            return OverviewStats(
                total_count=0,
                total_amount=0.0,
                average_amount=0.0,
                min_date=now,
                max_date=now,
            )

        total_count = len(transactions)
        total_amount = sum(t.amount for t in transactions)
        average_amount = total_amount / total_count if total_count > 0 else 0.0
        min_date = min(t.date for t in transactions)
        max_date = max(t.date for t in transactions)

        return OverviewStats(
            total_count=total_count,
            total_amount=total_amount,
            average_amount=average_amount,
            min_date=min_date,
            max_date=max_date,
        )
    
    def get_amount_distribution(self) -> AmountDistribution:
        """Récupérer les statistiques de distribution des montants.
        
        Calcule la distribution des transactions par plages de montants prédéfinies,
        y compris le nombre et le pourcentage pour chaque plage.
        
        Retours
        -------
        AmountDistribution
            Objet contenant la distribution des montants par plages.
        
        Exemples
        --------
        >>> service = StatisticsService(repository)
        >>> distribution = service.get_amount_distribution()
        >>> distribution.buckets[0].range
        '0-100'
        """
        transactions = self.repository.get_all_transactions()
        total_count = len(transactions)

        if total_count == 0:
            buckets = [
                AmountBucket(range=b["label"], count=0, percentage=0.0)
                for b in AMOUNT_BUCKETS
            ]
            return AmountDistribution(buckets=buckets)

        # Count transactions in each bucket
        bucket_counts: dict = defaultdict(int)
        for transaction in transactions:
            for bucket in AMOUNT_BUCKETS:
                if bucket["min"] <= transaction.amount < bucket["max"]:
                    bucket_counts[bucket["label"]] += 1
                    break

        # Create bucket responses
        buckets = []
        for bucket in AMOUNT_BUCKETS:
            count = bucket_counts[bucket["label"]]
            if total_count > 0:
                percentage = count / total_count * 100
            else:
                percentage = 0.0
            buckets.append(
                AmountBucket(
                    range=bucket["label"],
                    count=count,
                    percentage=percentage,
                )
            )

        return AmountDistribution(buckets=buckets)

    def get_stats_by_type(self) -> List[TypeStats]:
        """Récupérer les statistiques groupées par type de transaction.
        
        Calcule les statistiques pour chaque type de transaction (code de catégorie
        de commerçant), y compris le nombre, les montants totaux et moyens.
        
        Retours
        -------
        List[TypeStats]
            Liste des statistiques par type, triée par nombre décroissant.
        
        Exemples
        --------
        >>> service = StatisticsService(repository)
        >>> stats = service.get_stats_by_type()
        >>> stats[0].count >= stats[1].count
        True
        """
        types = self.repository.get_all_types()
        type_stats = []

        for mcc in types:
            transactions = self.repository.get_all_by_type(mcc)
            if transactions:
                count = len(transactions)
                total_amount = sum(t.amount for t in transactions)
                average_amount = total_amount / count if count > 0 else 0.0

                type_stats.append(
                    TypeStats(
                        type=mcc,
                        count=count,
                        total_amount=total_amount,
                        average_amount=average_amount,
                    )
                )

        # Sort by count descending
        type_stats.sort(key=lambda x: x.count, reverse=True)
        return type_stats
    
    def get_daily_stats(self) -> list[dict]:
        """Récupérer les statistiques quotidiennes groupées par date.
        
        Calcule les statistiques pour chaque jour, y compris le nombre de transactions,
        les montants totaux et moyens par jour.
        
        Retours
        -------
        list[dict]
            Liste des statistiques quotidiennes triées par date croissante.
        
        Exemples
        --------
        >>> service = StatisticsService(repository)
        >>> daily = service.get_daily_stats()
        >>> daily[0]["date"]
        '2023-01-01'
        """
        transactions = self.repository.get_all_transactions()

        # Group by date
        daily_data = defaultdict(list)
        for transaction in transactions:
            day = transaction.date.date()
            daily_data[day].append(transaction)

        # Create daily stats
        daily_stats = []
        for day in sorted(daily_data.keys()):
            transactions_on_day = daily_data[day]
            count = len(transactions_on_day)
            total_amount = sum(t.amount for t in transactions_on_day)
            average_amount = total_amount / count if count > 0 else 0.0

            daily_stats.append(
                {
                    "date": str(day),
                    "count": count,
                    "total_amount": total_amount,
                    "average_amount": average_amount,
                }
            )

        return daily_stats
