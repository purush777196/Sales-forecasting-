"""Shared Utilities Module.

Provides centralized database connection management, application logging,
and custom domain exceptions.
"""

from src.utils.exceptions import (
    ShopCastException,
    ConfigurationError,
    DatabaseConnectionError,
    DataProcessingError,
    ModelError,
)
from src.utils.logger import get_logger, setup_logging
from src.utils.database import DatabaseManager, get_db_manager

__all__ = [
    "ShopCastException",
    "ConfigurationError",
    "DatabaseConnectionError",
    "DataProcessingError",
    "ModelError",
    "get_logger",
    "setup_logging",
    "DatabaseManager",
    "get_db_manager",
]

