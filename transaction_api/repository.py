"""Référentiel de transactions pour l'accès aux données.

Ce module fournit la classe TransactionRepository pour gérer les données de transaction,
y compris le chargement à partir d'un CSV, l'indexation, la recherche et la récupération
de transactions avec diverses options de filtrage et de pagination.

Classes
-------
TransactionRepository
    Référentiel pour gérer et accéder aux données de transaction.
"""

import csv
from collections import defaultdict
from datetime import datetime
from typing import Dict, List, Optional, Tuple

import pandas as pd

from transaction_api.config import CHUNK_SIZE
from transaction_api.exceptions import InvalidTransactionData
from transaction_api.logging_config import get_logger
from transaction_api.models import SearchFilters, Transaction

logger = get_logger(__name__)


class TransactionRepository:
    """Référentiel pour gérer les transactions.
    
    Gère les données de transaction avec plusieurs index pour une interrogation efficace
    par client, commerçant, type et autres attributs. Supporte le chargement à partir
    d'un CSV, la recherche avec filtres et la pagination.
    
    Attributs
    ---------
    transactions : Dict[str, Transaction]
        Dictionnaire mappant les ID de transaction aux objets Transaction.
    customer_index : Dict[str, List[str]]
        Index mappant les ID client aux listes d'ID de transaction.
    merchant_index : Dict[str, List[str]]
        Index mappant les ID commerçant aux listes d'ID de transaction.
    date_index : List[str]
        Liste des ID de transaction triés par date.
    type_index : Dict[str, List[str]]
        Index mappant les codes de catégorie de commerçant aux listes d'ID de transaction.
    use_chip_index : Dict[str, List[str]]
        Index mappant les types use_chip aux listes d'ID de transaction.
    fraud_index : List[str]
        Liste des ID de transaction signalés comme frauduleux.
    data_load_date : datetime, optionnel
        Quand les données de transaction ont été chargées.
    min_date : datetime, optionnel
        Date de transaction la plus ancienne du référentiel.
    max_date : datetime, optionnel
        Date de transaction la plus récente du référentiel.
    """

    def __init__(self) -> None:
        """Initialiser le référentiel.
        
        Crée des structures de données vides pour stocker les transactions et les index.
        """
        self.transactions: Dict[str, Transaction] = {}
        self.customer_index: Dict[str, List[str]] = defaultdict(list)
        self.merchant_index: Dict[str, List[str]] = defaultdict(list)
        self.date_index: List[str] = []
        self.type_index: Dict[str, List[str]] = defaultdict(list)
        self.use_chip_index: Dict[str, List[str]] = defaultdict(list)
        self.fraud_index: List[str] = []
        self.data_load_date: Optional[datetime] = None
        self.min_date: Optional[datetime] = None
        self.max_date: Optional[datetime] = None

    def load_from_csv(self, filepath: Optional[str] = None) -> None:
        """Charger les transactions à partir d'un fichier CSV.
        
        Charge les données de transaction à partir d'un fichier CSV, analyse chaque ligne
        et remplit le référentiel avec les transactions et les index. Enregistre la
        progression et les erreurs.
        
        Paramètres
        ----------
        filepath : str, optionnel
            Chemin vers le fichier CSV. Par défaut "./data/transactions.csv".
        
        Lève
        ----
        FileNotFoundError
            Si le fichier CSV n'existe pas.
        InvalidTransactionData
            Si le fichier CSV n'a pas d'en-têtes ou contient des données invalides.
        
        Exemples
        --------
        >>> repo = TransactionRepository()
        >>> repo.load_from_csv("data/transactions.csv")
        """
        if filepath is None:
            filepath = "./data/transactions.csv"

        logger.info(f"Loading transactions from {filepath}")
        loaded_count = 0
        error_count = 0

        try:
            with open(filepath, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                if reader.fieldnames is None:
                    raise InvalidTransactionData("CSV file has no headers")

                for row_num, row in enumerate(reader, start=2):
                    try:
                        # Skip empty rows
                        if not row or not row.get("id", "").strip():
                            continue

                        transaction = self._parse_transaction(row)
                        self._add_transaction(transaction)
                        loaded_count += 1

                        if loaded_count % CHUNK_SIZE == 0:
                            logger.info(f"Loaded {loaded_count} transactions")
                    except Exception as e:
                        error_count += 1
                        logger.warning(
                            f"Error loading transaction at row {row_num}: {e}"
                        )

            self.data_load_date = datetime.utcnow()
            logger.info(f"Transaction :{loaded_count}. Error: {error_count}")
        except FileNotFoundError:
            logger.error(f"CSV file not found: {filepath}")
            raise
        except Exception as e:
            logger.error(f"Error loading CSV file: {e}")
            raise

    def _parse_transaction(self, row: Dict[str, str]) -> Transaction:
        """Analyser une transaction à partir d'une ligne CSV.
        
        Analyse un dictionnaire de ligne CSV en un objet Transaction, en gérant
        les conversions de type et la validation des données.
        
        Paramètres
        ----------
        row : Dict[str, str]
            Dictionnaire représentant une ligne CSV avec les données de transaction.
        
        Retours
        -------
        Transaction
            Objet Transaction analysé.
        
        Lève
        ----
        InvalidTransactionData
            Si la ligne contient des données invalides ou manquantes requises.
        """
        try:
            # Get date string and handle empty values
            date_str = row.get("date", "").strip()
            if not date_str:
                raise ValueError("Date is empty")

            date_obj = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")

            # Parse amount - remove $ if present
            amount_str = row.get("amount", "0").strip()
            if amount_str.startswith("$"):
                amount_str = amount_str[1:]
            amount = float(amount_str)
            use_chip = row.get("use_chip", "").strip()

            # Get ID and handle empty values
            transaction_id = row.get("id", "").strip()
            if not transaction_id:
                raise ValueError("Transaction ID is empty")

            transaction = Transaction(
                id=transaction_id,
                date=date_obj,
                client_id=row.get("client_id", "").strip(),
                card_id=row.get("card_id", "").strip(),
                amount=amount,
                use_chip=use_chip,
                merchant_id=row.get("merchant_id", "").strip(),
                merchant_city=row.get("merchant_city", "").strip(),
                merchant_state=row.get("merchant_state", "").strip(),
                zip=row.get("zip", "").strip(),
                mcc=row.get("mcc", "").strip(),
                errors=row.get("errors", "").strip() or None,
            )
            return transaction
        except (ValueError, KeyError) as e:
            raise InvalidTransactionData(f"Invalid transaction data: {e}")

    def _add_transaction(self, transaction: Transaction) -> None:
        """Ajouter une transaction au référentiel.
        
        Ajoute une transaction au référentiel et met à jour tous les index.
        Met à jour les dates min/max si nécessaire.
        
        Paramètres
        ----------
        transaction : Transaction
            La transaction à ajouter.
        """
        self.transactions[transaction.id] = transaction
        self.customer_index[transaction.client_id].append(transaction.id)
        self.merchant_index[transaction.merchant_id].append(transaction.id)
        self.type_index[transaction.mcc].append(transaction.id)
        self.use_chip_index[transaction.use_chip].append(transaction.id)
        self.date_index.append(transaction.id)

        if transaction.errors:
            self.fraud_index.append(transaction.id)

        if self.min_date is None or transaction.date < self.min_date:
            self.min_date = transaction.date
        if self.max_date is None or transaction.date > self.max_date:
            self.max_date = transaction.date

    def get_all_transactions(self) -> List[Transaction]:
        """Obtenir toutes les transactions.
        
        Retours
        -------
        List[Transaction]
            Liste de toutes les transactions du référentiel.
        """
        return list(self.transactions.values())

    def get_all(
        self, page: int = 1, limit: int = 50
    ) -> Tuple[List[Transaction], int]:
        """Obtenir les transactions paginées.
        
        Récupère toutes les transactions avec pagination, triées par date en ordre décroissant.
        
        Paramètres
        ----------
        page : int, optionnel
            Numéro de page (indexé à partir de 1). Par défaut 1.
        limit : int, optionnel
            Nombre d'éléments par page. Par défaut 50.
        
        Retours
        -------
        Tuple[List[Transaction], int]
            Tuple de (transactions pour la page, nombre total).
        """
        if page < 1:
            page = 1
        if limit < 1 or limit > 1000:
            limit = 50

        offset = (page - 1) * limit
        all_transactions = sorted(
            self.transactions.values(),
            key=lambda t: t.date,
            reverse=True,
        )
        total_count = len(all_transactions)
        transactions = all_transactions[offset: offset + limit]
        return transactions, total_count

    def get_by_id(self, transaction_id: str) -> Optional[Transaction]:
        """Obtenir une transaction par ID.
        
        Paramètres
        ----------
        transaction_id : str
            L'ID de transaction à récupérer.
        
        Retours
        -------
        Transaction, optionnel
            La transaction si trouvée, None sinon.
        """
        return self.transactions.get(transaction_id)

    def search(
        self, filters: SearchFilters, page: int = 1, limit: int = 50
    ) -> Tuple[List[Transaction], int]:
        """Rechercher les transactions avec des filtres.
        
        Recherche les transactions en utilisant les filtres fournis et retourne les
        résultats paginés.
        
        Paramètres
        ----------
        filters : SearchFilters
            Critères de filtre de recherche.
        page : int, optionnel
            Numéro de page (indexé à partir de 1). Par défaut 1.
        limit : int, optionnel
            Nombre d'éléments par page. Par défaut 50.
        
        Retours
        -------
        Tuple[List[Transaction], int]
            Tuple de (transactions filtrées pour la page, nombre total).
        """
        if page < 1:
            page = 1
        if limit < 1 or limit > 1000:
            limit = 50

        # Start with all transactions
        results = list(self.transactions.values())
        self.df = pd.DataFrame([vars(t) for t in results])
        df1 = self.df.copy()

        # Initialize mask for filtering
        mask = pd.Series([True] * len(df1), index=df1.index)

        # Apply filters using mask
        if filters.client_id and filters.client_id not in ("", "string"):
            mask &= df1["client_id"] == str(filters.client_id)

        if filters.transaction_id and filters.transaction_id not in (
            "",
            "string",
        ):
            mask &= df1["id"] == str(filters.transaction_id)

        if filters.use_chip and filters.use_chip not in ("", "string"):
            mask &= df1["use_chip"] == str(filters.use_chip)

        if filters.merchant_city and filters.merchant_city not in (
            "",
            "string",
        ):
            mask &= df1["merchant_city"] == str(filters.merchant_city)
        if filters.min_amount is not None:
            mask &= df1["amount"] >= float(filters.min_amount)
        if filters.max_amount is not None:
            mask &= df1["amount"] <= float(filters.max_amount)

        # Apply mask to get filtered results
        df_filtered = df1[mask]
        # Convert filtered dataframe back to Transaction objects
        filtered_results: List[Transaction] = []
        for _, row in df_filtered.iterrows():
            transaction = Transaction(
                id=str(row["id"]),
                date=row["date"],
                client_id=str(row["client_id"]),
                card_id=str(row["card_id"]),
                amount=float(row["amount"]),
                use_chip=str(row["use_chip"]),
                merchant_id=str(row["merchant_id"]),
                merchant_city=str(row["merchant_city"]),
                merchant_state=str(row["merchant_state"]),
                zip=str(row["zip"]),
                mcc=str(row["mcc"]),
                errors=row["errors"] if pd.notna(row["errors"]) else None,
            )
            filtered_results.append(transaction)

        # Sort by date descending
        filtered_results = sorted(
            filtered_results,
            key=lambda t: t.date,
            reverse=True,
        )
        df_filtered = None

        # Apply pagination
        offset = (page - 1) * limit
        total_count = len(filtered_results)
        paginated_results = filtered_results[offset: offset + limit]

        return paginated_results, total_count

    def delete(self, transaction_id: str) -> None:
        """Supprimer une transaction.
        
        Supprime une transaction du référentiel et de tous les index.
        
        Paramètres
        ----------
        transaction_id : str
            L'ID de la transaction à supprimer.
        """
        if transaction_id not in self.transactions:
            return

        transaction = self.transactions[transaction_id]

        # Remove from all indexes
        del self.transactions[transaction_id]
        self.customer_index[transaction.client_id].remove(transaction_id)
        self.merchant_index[transaction.merchant_id].remove(transaction_id)
        self.type_index[transaction.mcc].remove(transaction_id)
        self.use_chip_index[transaction.use_chip].remove(transaction_id)
        self.date_index.remove(transaction_id)

        if transaction.errors:
            self.fraud_index.remove(transaction_id)

    def get_by_customer(
        self, customer_id: str, page: int = 1, limit: int = 50
    ) -> Tuple[List[Transaction], int]:
        """Obtenir les transactions pour un client.
        
        Récupère toutes les transactions pour un client spécifique avec pagination.
        
        Paramètres
        ----------
        customer_id : str
            L'ID du client pour lequel récupérer les transactions.
        page : int, optionnel
            Numéro de page (indexé à partir de 1). Par défaut 1.
        limit : int, optionnel
            Nombre d'éléments par page. Par défaut 50.
        
        Retours
        -------
        Tuple[List[Transaction], int]
            Tuple de (transactions du client pour la page, nombre total).
        """
        if page < 1:
            page = 1
        if limit < 1 or limit > 1000:
            limit = 50

        transaction_ids = self.customer_index.get(customer_id, [])
        transactions = [
            self.transactions[tid]
            for tid in transaction_ids
            if tid in self.transactions
        ]
        transactions = sorted(transactions, key=lambda t: t.date, reverse=True)

        offset = (page - 1) * limit
        total_count = len(transactions)
        paginated_transactions = transactions[offset: offset + limit]

        return paginated_transactions, total_count

    def get_by_merchant(
        self, merchant_id: str, page: int = 1, limit: int = 50
    ) -> Tuple[List[Transaction], int]:
        """Obtenir les transactions pour un commerçant.
        
        Récupère toutes les transactions pour un commerçant spécifique avec pagination.
        
        Paramètres
        ----------
        merchant_id : str
            L'ID du commerçant pour lequel récupérer les transactions.
        page : int, optionnel
            Numéro de page (indexé à partir de 1). Par défaut 1.
        limit : int, optionnel
            Nombre d'éléments par page. Par défaut 50.
        
        Retours
        -------
        Tuple[List[Transaction], int]
            Tuple de (transactions du commerçant pour la page, nombre total).
        """
        if page < 1:
            page = 1
        if limit < 1 or limit > 1000:
            limit = 50

        transaction_ids = self.merchant_index.get(merchant_id, [])
        transactions = [
            self.transactions[tid]
            for tid in transaction_ids
            if tid in self.transactions
        ]
        transactions = sorted(
            transactions,
            key=lambda t: t.date,
            reverse=True,
        )

        offset = (page - 1) * limit
        total_count = len(transactions)
        paginated_transactions = transactions[offset: offset + limit]

        return paginated_transactions, total_count

    def get_all_by_type(self, mcc: str) -> List[Transaction]:
        """Obtenir toutes les transactions d'un type spécifique.
        
        Récupère toutes les transactions avec un code de catégorie de commerçant spécifique.
        
        Paramètres
        ----------
        mcc : str
            Le code de catégorie de commerçant pour filtrer.
        
        Retours
        -------
        List[Transaction]
            Liste des transactions avec le MCC spécifié.
        """
        transaction_ids = self.type_index.get(mcc, [])
        return [
            self.transactions[tid]
            for tid in transaction_ids
            if tid in self.transactions
        ]

    def get_fraud_transactions(self) -> List[Transaction]:
        """Obtenir toutes les transactions frauduleuses.
        
        Retours
        -------
        List[Transaction]
            Liste de toutes les transactions signalées comme frauduleuses.
        """
        return [
            self.transactions[tid]
            for tid in self.fraud_index
            if tid in self.transactions
        ]

    def get_all_types(self) -> List[str]:
        """Obtenir tous les types de transaction uniques.
        
        Retours
        -------
        List[str]
            Liste de tous les codes de catégorie de commerçant uniques.
        """
        return list(self.type_index.keys())

    def get_all_customers(self) -> List[str]:
        """Obtenir tous les ID client uniques.
        
        Retours
        -------
        List[str]
            Liste de tous les ID client uniques du référentiel.
        """
        return list(self.customer_index.keys())

    def get_all_use_chip_types(self) -> List[str]:
        """Obtenir tous les types use_chip uniques.
        
        Retours
        -------
        List[str]
            Liste de tous les types use_chip uniques.
        """
        return list(self.use_chip_index.keys())

    def get_all_by_use_chip(self, use_chip: str) -> List[Transaction]:
        """Obtenir toutes les transactions d'un type use_chip spécifique.
        
        Récupère toutes les transactions avec un type use_chip spécifique.
        
        Paramètres
        ----------
        use_chip : str
            Le type use_chip pour filtrer.
        
        Retours
        -------
        List[Transaction]
            Liste des transactions avec le type use_chip spécifié.
        """
        transaction_ids = self.use_chip_index.get(use_chip, [])
        return [
            self.transactions[tid]
            for tid in transaction_ids
            if tid in self.transactions
        ]
