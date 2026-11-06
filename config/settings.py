"""Centralized Application Configuration for ShopCast.

Implements environment-driven, type-validated settings using Pydantic Settings.
Credentials and environment overrides are loaded from `.env` files or system
environment variables without hardcoding secrets.
"""

from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path
from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

# Base directory of the repository (where config/ resides one level below root)
BASE_DIR = Path(__file__).resolve().parent.parent


class DatabaseSettings(BaseSettings):
    """MySQL Database connection and pool settings."""

    model_config = SettingsConfigDict(
        env_file=str(BASE_DIR / ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
        env_prefix="DB_",
    )

    host: str = Field(default="localhost", description="Database host server")
    port: int = Field(default=3306, description="Database port number")
    name: str = Field(default="shopcast_db", description="Database schema name")
    user: str = Field(default="shopcast_user", description="Database username")
    password: str = Field(default="", description="Database user password")
    pool_size: int = Field(default=5, description="Connection pool size")
    max_overflow: int = Field(default=10, description="Max overflow connections")
    pool_timeout: int = Field(default=30, description="Pool timeout in seconds")

    @property
    def connection_url(self) -> str:
        """Construct a SQLAlchemy connection string using pymysql."""
        # Note: password is URL-encoded by SQLAlchemy when passed as URL object,
        # but for simple pymysql connection strings we format standard URI.
        return f"mysql+pymysql://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}?charset=utf8mb4"

    @property
    def safe_connection_url(self) -> str:
        """Construct a masked connection string safe for logging and display."""
        masked_pwd = "******" if self.password else ""
        return f"mysql+pymysql://{self.user}:{masked_pwd}@{self.host}:{self.port}/{self.name}"


class AppSettings(BaseSettings):
    """Primary application configuration aggregating all sub-settings."""

    model_config = SettingsConfigDict(
        env_file=str(BASE_DIR / ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # General Application Settings
    app_name: str = Field(default="ShopCast", alias="APP_NAME")
    app_env: str = Field(default="development", alias="APP_ENV")
    debug: bool = Field(default=True, alias="DEBUG")

    # Logging
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")
    log_file_path: Optional[str] = Field(
        default=str(BASE_DIR / "reports" / "shopcast.log"),
        alias="LOG_FILE_PATH",
    )

    # Repository Paths
    base_dir: Path = BASE_DIR
    data_raw_dir: Path = Field(default=BASE_DIR / "data" / "raw", alias="DATA_RAW_DIR")
    data_processed_dir: Path = Field(
        default=BASE_DIR / "data" / "processed", alias="DATA_PROCESSED_DIR"
    )
    data_external_dir: Path = Field(
        default=BASE_DIR / "data" / "external", alias="DATA_EXTERNAL_DIR"
    )
    models_dir: Path = Field(default=BASE_DIR / "models", alias="MODELS_DIR")
    reports_dir: Path = Field(default=BASE_DIR / "reports", alias="REPORTS_DIR")

    # Forecasting Configuration
    forecast_horizon_days: int = Field(default=30, alias="FORECAST_HORIZON_DAYS")
    random_seed: int = Field(default=42, alias="RANDOM_SEED")

    # Nested Database Settings
    db: DatabaseSettings = Field(default_factory=DatabaseSettings)


@lru_cache(maxsize=1)
def get_settings() -> AppSettings:
    """Retrieve and cache the application settings singleton."""
    return AppSettings()

