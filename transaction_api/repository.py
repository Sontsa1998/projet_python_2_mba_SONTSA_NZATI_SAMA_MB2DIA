"""Transaction repository for data access."""

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
    """Repository for managing transactions."""

    def __init__(self) -> None:
        """Initialize the repository."""
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
        """Load transactions from CSV file."""
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
        """Parse a transaction from a CSV row."""
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
        """Add a transaction to the repository."""
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
        """Get all transactions."""
        return list(self.transactions.values())

    def get_all(
        self, page: int = 1, limit: int = 50
    ) -> Tuple[List[Transaction], int]:
        """Get paginated transactions."""
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
        """Get a transaction by ID."""
        return self.transactions.get(transaction_id)
    
    