"""Service de détection de fraude pour la logique métier.

Ce module fournit la classe FraudService qui gère les opérations de détection de fraude,
y compris l'analyse des transactions frauduleuses et la prédiction des risques de fraude.

Classes
-------
FraudService
    Service pour les opérations de détection de fraude.
"""

from typing import List

from transaction_api.logging_config import get_logger
from transaction_api.models import (
    FraudPrediction,
    FraudSummary,
    FraudTypeStats,
    Transaction,
)
from transaction_api.repository import TransactionRepository

logger = get_logger(__name__)


class FraudService:
    """Service pour les opérations de détection de fraude.
    
    Gère les opérations de détection de fraude, y compris l'analyse des transactions
    frauduleuses, le calcul des taux de fraude et la prédiction des risques de fraude.
    
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

    def get_fraud_summary(self) -> FraudSummary:
        """Récupérer le résumé de la détection de fraude.
        
        Calcule et retourne un résumé des statistiques de fraude, y compris le nombre
        total de transactions frauduleuses, le taux de fraude et le montant total frauduleux.
        
        Retours
        -------
        FraudSummary
            Résumé contenant les statistiques de fraude.
        
        Exemples
        --------
        >>> service = FraudService(repository)
        >>> summary = service.get_fraud_summary()
        >>> summary.fraud_rate
        0.05
        """
        transactions = self.repository.get_all_transactions()
        fraud_transactions = self.repository.get_fraud_transactions()

        total_count = len(transactions)
        fraud_count = len(fraud_transactions)
        if total_count > 0:
            fraud_rate = fraud_count / total_count
        else:
            fraud_rate = 0.0
        total_fraud_amount = sum(t.amount for t in fraud_transactions)

        return FraudSummary(
            total_fraud_count=fraud_count,
            fraud_rate=fraud_rate,
            total_fraud_amount=total_fraud_amount,
        )

    def get_fraud_by_type(self) -> List[FraudTypeStats]:
        """Récupérer les statistiques de fraude groupées par type de transaction.
        
        Calcule les statistiques de fraude pour chaque type de transaction (use_chip),
        y compris le nombre de fraudes et le taux de fraude.
        
        Retours
        -------
        List[FraudTypeStats]
            Liste des statistiques de fraude par type, triée par taux de fraude décroissant.
        
        Exemples
        --------
        >>> service = FraudService(repository)
        >>> stats = service.get_fraud_by_type()
        >>> stats[0].fraud_rate >= stats[1].fraud_rate
        True
        """
        use_chip_types = self.repository.get_all_use_chip_types()
        fraud_stats = []

        for use_chip in use_chip_types:
            transactions = self.repository.get_all_by_use_chip(use_chip)
            fraud_transactions = [t for t in transactions if t.errors]

            if transactions:
                fraud_count = len(fraud_transactions)
                total_count = len(transactions)
                if total_count > 0:
                    fraud_rate = fraud_count / total_count
                else:
                    fraud_rate = 0.0

                fraud_stats.append(
                    FraudTypeStats(
                        type=use_chip,
                        fraud_count=fraud_count,
                        fraud_rate=fraud_rate,
                        total_count=total_count,
                    )
                )

        # Sort by fraud rate descending
        fraud_stats.sort(key=lambda x: x.fraud_rate, reverse=True)
        return fraud_stats

    def predict_fraud(self, transaction: Transaction) -> FraudPrediction:
        """Prédire le risque de fraude pour une transaction.
        
        Analyse une transaction et calcule un score de risque de fraude basé sur
        plusieurs indicateurs, puis génère une explication du résultat.
        
        Paramètres
        ----------
        transaction : Transaction
            La transaction à analyser.
        
        Retours
        -------
        FraudPrediction
            Prédiction contenant le score de fraude et le raisonnement.
        
        Exemples
        --------
        >>> service = FraudService(repository)
        >>> prediction = service.predict_fraud(transaction)
        >>> prediction.fraud_score
        0.8
        """
        score = self._calculate_fraud_score(transaction)
        reasoning = self._generate_reasoning(transaction, score)

        return FraudPrediction(fraud_score=score, reasoning=reasoning)

    def _calculate_fraud_score(self, transaction: Transaction) -> float:
        """Calculer le score de fraude pour une transaction.
        
        Calcule un score de fraude entre 0.0 et 1.0 basé sur plusieurs indicateurs
        tels que la présence d'erreurs, le montant et l'utilisation de la puce.
        
        Paramètres
        ----------
        transaction : Transaction
            La transaction à analyser.
        
        Retours
        -------
        float
            Score de fraude entre 0.0 (pas de fraude) et 1.0 (fraude certaine).
        """
        score = 0.0

        # Check if transaction has errors field
        if transaction.errors:
            score += 0.8

        # Check amount - very high amounts are suspicious
        if transaction.amount > 5000:
            score += 0.2
        elif transaction.amount > 2000:
            score += 0.1

        # Check if chip was not used - higher fraud risk
        if not transaction.use_chip:
            score += 0.1

        # Ensure score is between 0 and 1
        return min(1.0, max(0.0, score))

    def _generate_reasoning(
        self, transaction: Transaction, score: float
    ) -> str:
        """Générer le raisonnement pour la prédiction de fraude.
        
        Génère une explication textuelle des indicateurs de fraude détectés
        pour justifier le score de fraude calculé.
        
        Paramètres
        ----------
        transaction : Transaction
            La transaction analysée.
        score : float
            Le score de fraude calculé.
        
        Retours
        -------
        str
            Explication textuelle du raisonnement de la prédiction.
        """
        reasons = []

        if transaction.errors:
            reasons.append(f"Has error flag: {transaction.errors}")

        if transaction.amount > 5000:
            reasons.append(f"High amount: ${transaction.amount:.2f}")
        elif transaction.amount > 2000:
            reasons.append(f"Moderate amount: ${transaction.amount:.2f}")

        if not transaction.use_chip:
            reasons.append("Chip was not used")

        if not reasons:
            reasons.append("No fraud indicators detected")

        reasoning = "; ".join(reasons)
        return reasoning
