"""Tests verifying the repository structure, required files, and package imports."""

import importlib
from pathlib import Path

from config.settings import BASE_DIR


def test_directory_structure_exists():
    """Verify that all required directories exist in the project."""
    expected_directories = [
        BASE_DIR / "data" / "raw",
        BASE_DIR / "data" / "processed",
        BASE_DIR / "data" / "external",
        BASE_DIR / "database" / "schema",
        BASE_DIR / "database" / "queries",
        BASE_DIR / "database" / "migrations",
        BASE_DIR / "notebooks",
        BASE_DIR / "src" / "data_ingestion",
        BASE_DIR / "src" / "preprocessing",
        BASE_DIR / "src" / "analysis",
        BASE_DIR / "src" / "features",
        BASE_DIR / "src" / "forecasting",
        BASE_DIR / "src" / "evaluation",
        BASE_DIR / "src" / "utils",
        BASE_DIR / "models",
        BASE_DIR / "powerbi",
        BASE_DIR / "reports",
        BASE_DIR / "tests",
        BASE_DIR / "docs",
        BASE_DIR / "config",
    ]

    for directory in expected_directories:
        assert directory.exists(), f"Directory missing: {directory}"
        assert directory.is_dir(), f"Path is not a directory: {directory}"


def test_required_root_files_exist():
    """Verify that required project root and documentation files exist."""
    expected_files = [
        BASE_DIR / "requirements.txt",
        BASE_DIR / ".env.example",
        BASE_DIR / ".gitignore",
        BASE_DIR / "README.md",
        BASE_DIR / "main.py",
        BASE_DIR / "docs" / "PROJECT_ARCHITECTURE.md",
    ]

    for file_path in expected_files:
        assert file_path.exists(), f"Required file missing: {file_path}"
        assert file_path.is_file(), f"Path is not a file: {file_path}"


def test_package_imports():
    """Verify that all Python subpackages under src/ are importable."""
    modules_to_test = [
        "src",
        "src.data_ingestion",
        "src.preprocessing",
        "src.analysis",
        "src.features",
        "src.forecasting",
        "src.evaluation",
        "src.utils",
        "src.utils.logger",
        "src.utils.database",
        "src.utils.exceptions",
        "config",
        "config.settings",
    ]

    for mod_name in modules_to_test:
        mod = importlib.import_module(mod_name)
        assert mod is not None, f"Failed to import module: {mod_name}"


def test_core_dependencies_importable():
    """Verify that all technology stack libraries are installed and importable."""
    dependencies = [
        "pandas",
        "numpy",
        "sklearn",
        "xgboost",
        "prophet",
        "sqlalchemy",
        "pymysql",
        "pydantic",
        "pydantic_settings",
        "dotenv",
        "pytest",
    ]

    for dep in dependencies:
        mod = importlib.import_module(dep)
        assert mod is not None, f"Technology stack dependency missing: {dep}"

