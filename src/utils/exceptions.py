"""Custom Domain Exceptions for ShopCast.

Provides a structured exception hierarchy for application-wide error handling,
ensuring failures are explicit, informative, and traceable.
"""


class ShopCastException(Exception):
    """Base exception for all ShopCast application errors."""

    def __init__(self, message: str, details: dict | None = None) -> None:
        super().__init__(message)
        self.message = message
        self.details = details or {}

    def __str__(self) -> str:
        if self.details:
            return f"{self.message} | Details: {self.details}"
        return self.message


class ConfigurationError(ShopCastException):
    """Raised when environment variables or application configuration is invalid or missing."""
    pass


class DatabaseConnectionError(ShopCastException):
    """Raised when establishing or executing operations on the database fails."""
    pass


class DataProcessingError(ShopCastException):
    """Raised when data cleansing, feature generation, or transformation fails."""
    pass


class DataIngestionError(ShopCastException):
    """Raised when ingesting data from external or raw sources fails."""
    pass


class ModelError(ShopCastException):
    """Raised during model training, evaluation, or inference errors."""
    pass

