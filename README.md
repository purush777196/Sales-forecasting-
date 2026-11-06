# ShopCast – Sales Forecasting & Business Intelligence System

[![Python 3.13+](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![MySQL 8.0+](https://img.shields.io/badge/mysql-8.0+-orange.svg)](https://www.mysql.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code Style: Clean](https://img.shields.io/badge/code%20style-pep8-green.svg)](https://pep8.org/)

ShopCast is a production-grade sales forecasting and business intelligence system engineered specifically for local retail shops and small-to-medium retail businesses. The system combines statistical and machine learning forecasting models (Prophet and XGBoost) with a MySQL dimensional data warehouse and Power BI interactive decision-support dashboards.

---

## 📌 Business Problem & Objectives

Local retail merchants face daily inventory volatility:
- **Stockouts**: Sudden demand spikes exhaust popular inventory, losing high-margin sales and diminishing customer loyalty.
- **Overstocking**: Excessive inventory ties up working capital and leads to product degradation, obsolescence, or aggressive markdown losses.

### Objectives
1. **Automated Demand Forecasting**: Generate 7-day, 14-day, and 30-day ahead forecasts at both the item (SKU) and store/category levels.
2. **Dynamic Inventory Optimization**: Provide automated safety stock and reorder point recommendations.
3. **Interactive BI Dashboards**: Deliver Power BI reports tracking gross margin, sell-through velocity, forecast accuracy (MAPE/RMSE), and seasonal trends.

---

## 🛠️ Technology Stack

- **Core Analytics & Orchestration**: Python 3.13+
- **Data Engineering**: Pandas, NumPy
- **Relational Data Warehouse**: MySQL 8.0+
- **Database ORM & Drivers**: SQLAlchemy 2.0+, PyMySQL
- **Machine Learning**: Scikit-learn, XGBoost
- **Time-Series Forecasting**: Meta Prophet
- **Business Intelligence**: Microsoft Power BI Desktop
- **Configuration & Validation**: Pydantic Settings, Python-Dotenv
- **Testing**: Pytest

---

## 📂 Repository Structure

```text
Sales-forecasting-/
│
├── data/
│   ├── raw/                 # Raw point-of-sale exports (gitignored)
│   ├── processed/           # Transformed & feature-engineered data (gitignored)
│   └── external/            # External datasets (calendar events, holidays)
│
├── database/
│   ├── schema/              # DDL scripts (schema.sql) for MySQL tables
│   ├── queries/             # Analytical & diagnostic SQL queries
│   └── migrations/          # Schema migrations and versioning scripts
│
├── notebooks/               # Jupyter exploratory notebooks
│
├── src/
│   ├── data_ingestion/      # POS extractors and database batch loaders
│   ├── preprocessing/       # Outlier detection, cleaning, imputation
│   ├── analysis/            # Descriptive statistics & seasonal decomposition
│   ├── features/            # Lag, rolling window, calendar feature pipelines
│   ├── forecasting/         # Prophet, XGBoost, and ensemble forecasters
│   ├── evaluation/          # Backtesting and error metrics (MAE, RMSE, MAPE)
│   └── utils/               # Centralized logging, database pool, exceptions
│
├── models/                  # Serialized ML artifacts & scalers (gitignored)
├── powerbi/                 # Power BI templates (.pbit), schemas, and docs
├── reports/                 # Evaluation figures and execution logs
├── tests/                   # Pytest test suite
├── docs/                    # Architectural specs (PROJECT_ARCHITECTURE.md)
├── config/                  # Strongly typed application settings
│
├── requirements.txt         # Pinned project dependencies
├── .env.example             # Template for local environment variables
├── .gitignore               # Strict gitignore protecting secrets and data
├── README.md                # Project documentation and onboarding guide
└── main.py                  # Primary CLI application entrypoint
```

---

## 🚀 Quick Start Guide

### 1. Prerequisites
- **Python**: Version 3.13 or higher
- **MySQL Server**: Version 8.0 or higher
- **Git**: Installed and configured

### 2. Clone Repository & Switch Branch
```bash
git clone https://github.com/purush777196/Sales-forecasting-.git
cd Sales-forecasting-
git checkout -b feature/project-initialization
```

### 3. Create & Activate Virtual Environment
```bash
# Windows (PowerShell)
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Linux / macOS
python3 -m venv .venv
source .venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 5. Environment Configuration
Copy `.env.example` to `.env` and fill in your local MySQL credentials:
```bash
# Windows
copy .env.example .env

# Linux / macOS
cp .env.example .env
```

Edit `.env`:
```ini
APP_ENV=development
DEBUG=true
LOG_LEVEL=INFO

DB_HOST=localhost
DB_PORT=3306
DB_NAME=shopcast_db
DB_USER=root
DB_PASSWORD=your_local_password
```

### 6. Initialize MySQL Database (Optional for Phase 0)
```bash
mysql -u root -p < database/schema/schema.sql
```

### 7. Run Application Diagnostics
Run the built-in system check:
```bash
python main.py --check
```
*Tip: To skip the database probe while MySQL is offline, run `python main.py --check --no-db-check`.*

### 8. Run Unit Tests
```bash
pytest -v
```

---

## 🗺️ Implementation Roadmap

- [x] **Phase 0: Project Initialization** (Repository structure, environment, config, DB utilities, tests, architecture)
- [ ] **Phase 1: Data Ingestion & Database Schema** (Synthetic transaction generator, schema deployment, ETL loaders)
- [ ] **Phase 2: Exploratory Data Analysis & Preprocessing** (Cleaning, outlier filtering, EDA dashboards)
- [ ] **Phase 3: Feature Engineering** (Lags, rolling averages, seasonality indicators)
- [ ] **Phase 4: Forecasting Models** (Prophet baseline, XGBoost regressor, ensemble)
- [ ] **Phase 5: Model Evaluation & Reporting** (Time-series cross-validation, automated metric reports)
- [ ] **Phase 6: Power BI Integration & Deployment** (Interactive executive dashboards, automated pipelines)

---

## 🔒 Security Standards

- **Never commit `.env` files** or real database credentials.
- **Never commit raw customer or sales data** containing Personally Identifiable Information (PII).
- **Never commit large model binaries** (`.pkl`, `.joblib`) directly into Git. Use cloud artifact storage or the local `models/` folder ignored by `.gitignore`.

---

## 👥 Contributors & Contact

- **Repository**: [purush777196/Sales-forecasting-](https://github.com/purush777196/Sales-forecasting-)
- **Branch**: `feature/project-initialization`

