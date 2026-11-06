"""Centralized Logging Utility for ShopCast.

Provides consistent, formatted logging across all project modules with support
for both console streaming and persistent file rotation/output.
"""

from __future__ import annotations

import logging
import sys
from pathlib import Path
from typing import Optional

_DEFAULT_LOG_FORMAT = (
    "%(asctime)s | %(levelname)-8s | %(name)s:%(funcName)s:%(lineno)d - %(message)s"
)
_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def setup_logging(
    log_level: str = "INFO",
    log_file_path: Optional[str | Path] = None,
    log_format: str = _DEFAULT_LOG_FORMAT,
) -> logging.Logger:
    """Configure the root logger and return the main application logger.

    Args:
        log_level: Log severity string ('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL').
        log_file_path: Optional path to write log records to disk.
        log_format: Format string for log messages.

    Returns:
        logging.Logger: Configured root logger.
    """
    numeric_level = getattr(logging, log_level.upper(), logging.INFO)

    # Root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(numeric_level)

    # Avoid duplicate handlers if setup_logging is called multiple times
    if root_logger.hasHandlers():
        root_logger.handlers.clear()

    formatter = logging.Formatter(fmt=log_format, datefmt=_DATE_FORMAT)

    # Console Handler (writes to stdout)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(numeric_level)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)

    # File Handler (optional)
    if log_file_path:
        log_path = Path(log_file_path)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_path, encoding="utf-8")
        file_handler.setLevel(numeric_level)
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)

    return root_logger


def get_logger(name: str) -> logging.Logger:
    """Retrieve a namespaced logger instance.

    Args:
        name: Logger identifier, typically __name__.

    Returns:
        logging.Logger: Logger instance for the calling module.
    """
    return logging.getLogger(name)

