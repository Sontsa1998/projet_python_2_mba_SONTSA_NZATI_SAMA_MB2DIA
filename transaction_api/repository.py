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

    