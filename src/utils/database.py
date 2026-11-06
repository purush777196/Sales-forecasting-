"""MySQL Database Connection Utilities for ShopCast.

Provides managed SQLAlchemy connection pools, session contexts, and health checks
for MySQL operations without hardcoded credentials.
"""

from __future__ import annotations

from contextlib import contextmanager
from typing import Any, Dict, Generator, Optional

from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from sqlalchemy.exc import OperationalError, SQLAlchemyError
from sqlalchemy.orm import Session, sessionmaker

from config.settings import DatabaseSettings, get_settings
from src.utils.exceptions import DatabaseConnectionError
from src.utils.logger import get_logger

logger = get_logger(__name__)


class DatabaseManager:
    """Manages SQLAlchemy Engine, Session lifecycle, and connectivity checks."""

    def __init__(self, db_settings: Optional[DatabaseSettings] = None) -> None:
        """Initialize the DatabaseManager with explicit or environment settings.

        Args:
            db_settings: Optional DatabaseSettings instance. Defaults to loaded configuration.
        """
        self.settings: DatabaseSettings = db_settings or get_settings().db
        self._engine: Optional[Engine] = None
        self._session_factory: Optional[sessionmaker] = None

    @property
    def engine(self) -> Engine:
        """Lazily initialize and return the SQLAlchemy Engine with connection pooling."""
        if self._engine is None:
            try:
                self._engine = create_engine(
                    self.settings.connection_url,
                    pool_size=self.settings.pool_size,
                    max_overflow=self.settings.max_overflow,
                    pool_timeout=self.settings.pool_timeout,
                    pool_recycle=3600,
                    pool_pre_ping=True,
                    echo=False,
                )
                self._session_factory = sessionmaker(
                    bind=self._engine,
                    autocommit=False,
                    autoflush=False,
                )
                logger.debug(
                    "Initialized SQLAlchemy engine for: %s",
                    self.settings.safe_connection_url,
                )
            except Exception as exc:
                logger.error("Failed to initialize database engine: %s", exc)
                raise DatabaseConnectionError(
                    f"Could not initialize engine for {self.settings.safe_connection_url}",
                    details={"error": str(exc)},
                ) from exc
        return self._engine

    def test_connection(self) -> Dict[str, Any]:
        """Verify database reachability and authentication with a lightweight probe.

        Returns:
            Dict[str, Any]: Connection health details (status, message, host, schema).
        """
        result = {
            "connected": False,
            "host": self.settings.host,
            "port": self.settings.port,
            "database": self.settings.name,
            "message": "",
        }

        try:
            with self.engine.connect() as conn:
                probe = conn.execute(text("SELECT 1 AS probe"))
                row = probe.fetchone()
                if row and row[0] == 1:
                    result["connected"] = True
                    result["message"] = "Database connection established successfully."
                    logger.info("Database connection test succeeded: %s", self.settings.safe_connection_url)
                else:
                    result["message"] = "Probe query returned unexpected result."
                    logger.warning("Database probe failed with unexpected output.")
        except OperationalError as op_err:
            result["message"] = f"OperationalError: {op_err.orig if hasattr(op_err, 'orig') else str(op_err)}"
            logger.warning(
                "Database connection test failed for %s: %s",
                self.settings.safe_connection_url,
                result["message"],
            )
        except SQLAlchemyError as sql_err:
            result["message"] = f"SQLAlchemyError: {str(sql_err)}"
            logger.warning("Database test encountered error: %s", result["message"])
        except Exception as exc:
            result["message"] = f"Unexpected error: {str(exc)}"
            logger.error("Unexpected error during connection test: %s", exc)

        return result

    @contextmanager
    def get_connection(self) -> Generator[Any, None, None]:
        """Context manager providing an active database connection."""
        connection = None
        try:
            connection = self.engine.connect()
            yield connection
        except SQLAlchemyError as exc:
            logger.error("Database connection error: %s", exc)
            raise DatabaseConnectionError(
                "Failed to execute operation on database connection",
                details={"error": str(exc)},
            ) from exc
        finally:
            if connection is not None:
                connection.close()

    @contextmanager
    def get_session(self) -> Generator[Session, None, None]:
        """Context manager for SQLAlchemy ORM sessions with rollback on failure."""
        if self._session_factory is None:
            _ = self.engine  # Trigger engine & session factory initialization

        session: Session = self._session_factory()
        try:
            yield session
            session.commit()
        except Exception as exc:
            session.rollback()
            logger.error("Database session rollback triggered due to exception: %s", exc)
            raise DatabaseConnectionError(
                "Database transaction failed and was rolled back",
                details={"error": str(exc)},
            ) from exc
        finally:
            session.close()

    def close(self) -> None:
        """Dispose of the connection pool and close active connections."""
        if self._engine is not None:
            self._engine.dispose()
            self._engine = None
            self._session_factory = None
            logger.debug("Database engine pool disposed.")


_default_manager: Optional[DatabaseManager] = None


def get_db_manager(settings: Optional[DatabaseSettings] = None) -> DatabaseManager:
    """Retrieve or create the global DatabaseManager instance."""
    global _default_manager
    if _default_manager is None or settings is not None:
        _default_manager = DatabaseManager(db_settings=settings)
    return _default_manager

