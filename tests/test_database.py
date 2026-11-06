"""Tests for database utilities, connection pooling, and error handling."""

from unittest.mock import MagicMock, patch

import pytest
from sqlalchemy.exc import OperationalError

from config.settings import DatabaseSettings
from src.utils.database import DatabaseManager
from src.utils.exceptions import DatabaseConnectionError


def test_database_manager_engine_initialization(test_db_settings):
    """Verify that DatabaseManager initializes SQLAlchemy Engine with expected properties."""
    db_mgr = DatabaseManager(test_db_settings)
    engine = db_mgr.engine
    assert engine is not None
    assert str(engine.url).startswith("mysql+pymysql://test_user:")
    db_mgr.close()


def test_database_connection_test_failure_handling(test_db_settings):
    """Verify that test_connection returns structured failure without unhandled crash."""
    # Use invalid host/port to simulate offline MySQL
    offline_settings = DatabaseSettings(
        host="192.0.2.1",  # Test-net-1 reserved unroutable address
        port=3306,
        name="offline_db",
        user="nobody",
        password="bad",
        pool_timeout=1,
    )
    db_mgr = DatabaseManager(offline_settings)
    status = db_mgr.test_connection()
    assert status["connected"] is False
    assert status["host"] == "192.0.2.1"
    assert len(status["message"]) > 0
    db_mgr.close()


def test_database_connection_mock_success(test_db_settings):
    """Verify test_connection returns connected=True when probe returns 1."""
    db_mgr = DatabaseManager(test_db_settings)

    mock_connection = MagicMock()
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = (1,)
    mock_connection.execute.return_value = mock_cursor

    with patch.object(db_mgr.engine, "connect") as mock_connect:
        mock_connect.return_value.__enter__.return_value = mock_connection
        status = db_mgr.test_connection()
        assert status["connected"] is True
        assert "established" in status["message"].lower()

    db_mgr.close()


def test_database_get_connection_exception_wrapping(test_db_settings):
    """Verify that SQLAlchemy connection errors are cleanly wrapped in DatabaseConnectionError."""
    db_mgr = DatabaseManager(test_db_settings)

    with patch.object(db_mgr.engine, "connect", side_effect=OperationalError("mock fail", None, None)):
        with pytest.raises(DatabaseConnectionError):
            with db_mgr.get_connection():
                pass

    db_mgr.close()

