"""ShopCast - Sales Forecasting & Business Intelligence System.

Primary entrypoint and CLI interface for project lifecycle management,
environment diagnostics, and pipeline orchestration.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from config.settings import AppSettings, get_settings
from src.utils.database import get_db_manager
from src.utils.logger import get_logger, setup_logging

BANNER = r"""
  ____  _                 ____          _   
 / ___|| |__   ___  _ __ / ___|__ _ ___| |_ 
 \___ \| '_ \ / _ \| '_ \ |   / _` / __| __|
  ___) | | | | (_) | |_) | |__| (_| \__ \ |_ 
 |____/|_| |_|\___/| .__/ \____\__,_|___/\__|
                   |_|                       
  Sales Forecasting & Business Intelligence System
  Phase 0: Project Initialization
"""


def verify_directories(settings: AppSettings) -> dict[str, bool]:
    """Ensure all required project runtime directories exist on disk."""
    required_dirs = [
        settings.data_raw_dir,
        settings.data_processed_dir,
        settings.data_external_dir,
        settings.models_dir,
        settings.reports_dir,
    ]
    status = {}
    for dir_path in required_dirs:
        path_obj = Path(dir_path)
        path_obj.mkdir(parents=True, exist_ok=True)
        status[str(path_obj.name)] = path_obj.exists()
    return status


def run_diagnostics(settings: AppSettings, check_db: bool = True) -> int:
    """Run comprehensive environment, directory, and database diagnostics."""
    logger = get_logger("shopcast.diagnostics")

    print(BANNER)
    logger.info("Starting ShopCast diagnostics...")
    logger.info("Environment: %s | Debug: %s", settings.app_env, settings.debug)
    logger.info("Base Directory: %s", settings.base_dir)

    # 1. Directory Structure Verification
    dir_status = verify_directories(settings)
    all_dirs_ok = all(dir_status.values())
    logger.info("Directory check: %s (%s)", "PASS" if all_dirs_ok else "FAIL", dir_status)

    # 2. Database Connectivity Check
    db_ok = True
    if check_db:
        logger.info("Probing database connectivity (%s)...", settings.db.safe_connection_url)
        db_mgr = get_db_manager(settings.db)
        db_status = db_mgr.test_connection()
        if db_status["connected"]:
            logger.info("Database status: CONNECTED (%s)", db_status["message"])
        else:
            logger.warning(
                "Database status: OFFLINE/UNREACHABLE (%s). Configure .env when ready.",
                db_status["message"],
            )
            # Offline database in Phase 0 is non-fatal for environment bootstrap
            db_ok = False

    logger.info("ShopCast Phase 0 initialization check complete.")
    return 0


def main() -> int:
    """Main CLI entrypoint."""
    parser = argparse.ArgumentParser(
        description="ShopCast - Sales Forecasting & Business Intelligence CLI",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Run environment, directory, and system health checks.",
    )
    parser.add_argument(
        "--no-db-check",
        action="store_true",
        help="Skip database connection probe during check.",
    )
    parser.add_argument(
        "--version",
        action="version",
        version="ShopCast 0.1.0 (Phase 0: Initialization)",
    )

    args = parser.parse_args()

    # Load configuration & initialize logging
    settings = get_settings()
    setup_logging(log_level=settings.log_level, log_file_path=settings.log_file_path)

    # Default action: run system diagnostics
    check_db = not args.no_db_check
    return run_diagnostics(settings, check_db=check_db)


if __name__ == "__main__":
    sys.exit(main())

