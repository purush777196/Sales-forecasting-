"""Tests for configuration management and environment parsing."""

from pathlib import Path

from config.settings import AppSettings, DatabaseSettings, get_settings


def test_default_database_settings():
    """Verify default database settings and connection URL generation."""
    db = DatabaseSettings(
        host="localhost",
        port=3306,
        name="shopcast_db",
        user="root",
        password="secret_password",
    )
    assert db.host == "localhost"
    assert db.port == 3306
    assert db.name == "shopcast_db"
    assert "mysql+pymysql://root:secret_password@localhost:3306/shopcast_db" in db.connection_url
    assert "secret_password" not in db.safe_connection_url
    assert "******" in db.safe_connection_url


def test_app_settings_defaults():
    """Verify default application settings and base directories."""
    settings = get_settings()
    assert settings.app_name == "ShopCast"
    assert isinstance(settings.base_dir, Path)
    assert settings.base_dir.exists()
    assert settings.forecast_horizon_days == 30
    assert settings.random_seed == 42


def test_app_settings_environment_override(mock_env):
    """Verify that environment variables properly override settings."""
    settings = AppSettings()
    assert settings.app_env == "testing"
    assert settings.debug is False
    assert settings.log_level == "DEBUG"
    assert settings.db.host == "127.0.0.1"
    assert settings.db.name == "test_shopcast_db"
    assert settings.db.user == "test_user"
    assert settings.db.password == "test_secret_password"

