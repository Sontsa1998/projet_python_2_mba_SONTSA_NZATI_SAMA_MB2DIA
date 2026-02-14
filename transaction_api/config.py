"""Configuration and constants for the Transaction API."""

import os
from typing import Final

# API Configuration
API_VERSION: Final[str] = "1.0.0"
API_TITLE: Final[str] = "Transaction API"
API_DESCRIPTION: Final[str] = "High-performance API for transaction analysis"

# Data Configuration
CSV_FILE_PATH: Final[str] = os.getenv("CSV_FILE_PATH", "data/transactions.csv")
CHUNK_SIZE: Final[int] = 10000  # Number of rows to read at a time

# Pagination Configuration
DEFAULT_LIMIT: Final[int] = 50
MAX_LIMIT: Final[int] = 1000
MIN_LIMIT: Final[int] = 1

# Performance Configuration
RESPONSE_TIME_THRESHOLD_MS: Final[float] = 500.0
COMPLEX_QUERY_THRESHOLD_MS: Final[float] = 1000.0

# Amount Distribution Buckets
AMOUNT_BUCKETS: Final[list] = [
    {"min": 0, "max": 100, "label": "0-100"},
    {"min": 100, "max": 500, "label": "100-500"},
    {"min": 500, "max": 1000, "label": "500-1000"},
    {"min": 1000, "max": float("inf"), "label": "1000+"},
]

# Logging Configuration
LOG_LEVEL: Final[str] = os.getenv("LOG_LEVEL", "INFO")
LOG_FORMAT: Final[str] = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
