"""Application Configuration Module for ShopCast.

Provides strongly typed, environment-driven configuration management.
"""

from config.settings import AppSettings, DatabaseSettings, get_settings

__all__ = ["AppSettings", "DatabaseSettings", "get_settings"]

