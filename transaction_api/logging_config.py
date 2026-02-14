"""Logging configuration for the Transaction API."""

import logging
import logging.config
from typing import Dict, Any

from transaction_api.config import LOG_LEVEL, LOG_FORMAT


def setup_logging() -> None:
    """Set up logging configuration."""
    logging_config: Dict[str, Any] = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "standard": {
                "format": LOG_FORMAT,
            },
        },
        "handlers": {
            "default": {
                "level": LOG_LEVEL,
                "class": "logging.StreamHandler",
                "formatter": "standard",
            },
            "file": {
                "level": LOG_LEVEL,
                "class": "logging.FileHandler",
                "filename": "transaction_api.log",
                "formatter": "standard",
            },
        },
        "loggers": {
            "": {
                "handlers": ["default", "file"],
                "level": LOG_LEVEL,
                "propagate": True,
            },
        },
    }
    logging.config.dictConfig(logging_config)


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance."""
    return logging.getLogger(name)
