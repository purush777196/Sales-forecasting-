# Power BI Reporting Layer - ShopCast

This directory hosts business intelligence assets, report definitions, and integration guides for connecting Power BI to the ShopCast MySQL database and exported analytical datasets.

## Architecture

```
[ MySQL Database / Processed CSVs ]
                 │
                 ▼
    [ Power BI DirectQuery / Import ]
                 │
                 ├── 1. Executive Overview Dashboard
                 ├── 2. Sales Trend & Seasonality Visuals
                 ├── 3. Forecast vs. Actual Variance Tracking
                 └── 4. Inventory Reorder & Stockout Alerts
```

## Data Sources

1. **MySQL Direct Connection**:
   - Host: Configured via `.env` (`DB_HOST`)
   - Database: `shopcast_db`
   - Key Tables: `fact_sales`, `fact_forecasts`, `dim_products`, `dim_dates`, `fact_inventory`

2. **Processed Flat Files** (for offline demonstration):
   - Location: `data/processed/`
   - Format: Parquet or CSV with standard timestamps

## Report Pages Planned

- **Page 1: Sales Overview**: Gross revenue, transaction counts, AOV (Average Order Value), MoM/YoY growth.
- **Page 2: Forecasting Insights**: Prophet & XGBoost 30-day forecast curves, prediction intervals, MAPE tracking.
- **Page 3: Inventory Intelligence**: Reorder point indicators, slow-moving items, stockout risk alerts.

