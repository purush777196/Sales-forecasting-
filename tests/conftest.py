"""Pytest configuration and shared fixtures for ShopCast tests."""

import os
import pytest
from pathlib import Path

from config.settings import AppSettings, DatabaseSettings


@pytest.fixture
def mock_env(monkeypatch):
    """Provide an isolated environment for testing settings without touching production values."""
    monkeypatch.setenv("APP_ENV", "testing")
    monkeypatch.setenv("DEBUG", "false")
    monkeypatch.setenv("DB_HOST", "127.0.0.1")
    monkeypatch.setenv("DB_PORT", "3306")
    monkeypatch.setenv("DB_NAME", "test_shopcast_db")
    monkeypatch.setenv("DB_USER", "test_user")
    monkeypatch.setenv("DB_PASSWORD", "test_secret_password")
    monkeypatch.setenv("LOG_LEVEL", "DEBUG")


@pytest.fixture
def test_db_settings() -> DatabaseSettings:
    """Return explicit DatabaseSettings instance for testing."""
    return DatabaseSettings(
        host="127.0.0.1",
        port=3306,
        name="test_shopcast_db",
        user="test_user",
        password="test_secret_password",
    )


@pytest.fixture
def test_app_settings(test_db_settings) -> AppSettings:
    """Return explicit AppSettings instance for testing."""
    return AppSettings(
        app_name="ShopCast-Test",
        app_env="testing",
        debug=False,
        log_level="DEBUG",
        db=test_db_settings,
    )

