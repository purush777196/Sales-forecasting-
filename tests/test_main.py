"""Tests for main entrypoint, CLI arguments, and directory verification."""

import sys
from unittest.mock import patch

from config.settings import AppSettings
from main import main, run_diagnostics, verify_directories


def test_verify_directories(test_app_settings):
    """Verify that verify_directories creates and confirms directory existence."""
    status = verify_directories(test_app_settings)
    assert all(status.values()) is True


def test_run_diagnostics(test_app_settings):
    """Verify that run_diagnostics runs successfully without throwing."""
    exit_code = run_diagnostics(test_app_settings, check_db=False)
    assert exit_code == 0


def test_main_cli_execution(monkeypatch):
    """Verify that main() executes cleanly when called with --no-db-check."""
    monkeypatch.setattr(sys, "argv", ["main.py", "--check", "--no-db-check"])
    exit_code = main()
    assert exit_code == 0

