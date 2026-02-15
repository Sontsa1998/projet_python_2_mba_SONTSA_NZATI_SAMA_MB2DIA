"""Logging configuration for the Transaction API.

This module provides centralized logging configuration for the Transaction API,
setting up both console and file handlers with consistent formatting.

Functions
---------
setup_logging()
    Configure logging for the entire application.
get_logger(name)
    Get a logger instance for a specific module.
"""

import logging
import logging.config
from typing import Dict, Any

from transaction_api.config import LOG_LEVEL, LOG_FORMAT


def setup_logging() -> None:
    """Set up logging configuration.
    
    Configures logging with both console and file handlers using the settings
    from the config module. Creates a log file at 'transaction_api.log' and
    streams logs to the console with consistent formatting.
    
    Returns
    -------
    None
    
    Examples
    --------
    >>> setup_logging()
    >>> logger = get_logger(__name__)
    >>> logger.info("Application started")
    """
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
    """Get a logger instance.
    
    Returns a logger instance for the specified module name. The logger is
    configured with the settings established by setup_logging().
    
    Parameters
    ----------
    name : str
        The name of the logger, typically the module name (__name__).
    
    Returns
    -------
    logging.Logger
        A logger instance configured for the specified name.
    
    Examples
    --------
    >>> logger = get_logger(__name__)
    >>> logger.debug("Debug message")
    >>> logger.info("Info message")
    >>> logger.error("Error message")
    """
    return logging.getLogger(name)
