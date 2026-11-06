-- ==============================================================================
-- ShopCast - Initial Database Schema (MySQL 8.0+)
-- Phase 0: Database Preparation
-- ==============================================================================

CREATE DATABASE IF NOT EXISTS shopcast_db
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE shopcast_db;

-- ------------------------------------------------------------------------------
-- Dimension: Products
-- ------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS dim_products (
    product_id INT AUTO_INCREMENT PRIMARY KEY,
    sku VARCHAR(50) NOT NULL UNIQUE,
    product_name VARCHAR(150) NOT NULL,
    category VARCHAR(100) NOT NULL,
    subcategory VARCHAR(100) DEFAULT NULL,
    unit_cost DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
    unit_price DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
    reorder_level INT NOT NULL DEFAULT 10,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_products_category (category),
    INDEX idx_products_sku (sku)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ------------------------------------------------------------------------------
-- Dimension: Stores / Branches
-- ------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS dim_stores (
    store_id INT AUTO_INCREMENT PRIMARY KEY,
    store_code VARCHAR(20) NOT NULL UNIQUE,
    store_name VARCHAR(100) NOT NULL,
    city VARCHAR(100) NOT NULL,
    state VARCHAR(100) NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_stores_city (city)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ------------------------------------------------------------------------------
-- Dimension: Dates (Time Intelligence)
-- ------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS dim_dates (
    date_key INT PRIMARY KEY, -- e.g., YYYYMMDD
    full_date DATE NOT NULL UNIQUE,
    day_of_week TINYINT NOT NULL,
    day_name VARCHAR(15) NOT NULL,
    day_of_month TINYINT NOT NULL,
    month TINYINT NOT NULL,
    month_name VARCHAR(15) NOT NULL,
    quarter TINYINT NOT NULL,
    year SMALLINT NOT NULL,
    is_weekend BOOLEAN NOT NULL,
    is_holiday BOOLEAN NOT NULL DEFAULT FALSE,
    holiday_name VARCHAR(100) DEFAULT NULL,
    INDEX idx_dates_full_date (full_date),
    INDEX idx_dates_year_month (year, month)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ------------------------------------------------------------------------------
-- Fact: Daily Sales Transactions
-- ------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS fact_sales (
    sale_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    transaction_id VARCHAR(64) NOT NULL,
    transaction_date DATE NOT NULL,
    product_id INT NOT NULL,
    store_id INT NOT NULL,
    quantity INT NOT NULL,
    unit_price DECIMAL(10, 2) NOT NULL,
    discount_amount DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
    total_amount DECIMAL(12, 2) NOT NULL,
    payment_method VARCHAR(50) DEFAULT 'CASH',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_sales_product FOREIGN KEY (product_id) REFERENCES dim_products (product_id) ON DELETE RESTRICT,
    CONSTRAINT fk_sales_store FOREIGN KEY (store_id) REFERENCES dim_stores (store_id) ON DELETE RESTRICT,
    INDEX idx_sales_date (transaction_date),
    INDEX idx_sales_product_date (product_id, transaction_date),
    INDEX idx_sales_store_date (store_id, transaction_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ------------------------------------------------------------------------------
-- Fact: Inventory Snapshots
-- ------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS fact_inventory (
    inventory_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    snapshot_date DATE NOT NULL,
    product_id INT NOT NULL,
    store_id INT NOT NULL,
    stock_on_hand INT NOT NULL DEFAULT 0,
    stock_reserved INT NOT NULL DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_inventory_product FOREIGN KEY (product_id) REFERENCES dim_products (product_id) ON DELETE RESTRICT,
    CONSTRAINT fk_inventory_store FOREIGN KEY (store_id) REFERENCES dim_stores (store_id) ON DELETE RESTRICT,
    UNIQUE KEY uq_inventory_snapshot (snapshot_date, product_id, store_id),
    INDEX idx_inventory_date (snapshot_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ------------------------------------------------------------------------------
-- Fact: Forecast Predictions (Model Outputs)
-- ------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS fact_forecasts (
    forecast_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    model_name VARCHAR(50) NOT NULL,       -- e.g. 'prophet', 'xgboost', 'ensemble'
    model_version VARCHAR(20) NOT NULL,
    product_id INT NOT NULL,
    store_id INT NOT NULL,
    forecast_date DATE NOT NULL,
    predicted_quantity DECIMAL(10, 2) NOT NULL,
    lower_bound DECIMAL(10, 2) DEFAULT NULL,
    upper_bound DECIMAL(10, 2) DEFAULT NULL,
    generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_forecast_product FOREIGN KEY (product_id) REFERENCES dim_products (product_id) ON DELETE RESTRICT,
    CONSTRAINT fk_forecast_store FOREIGN KEY (store_id) REFERENCES dim_stores (store_id) ON DELETE RESTRICT,
    INDEX idx_forecast_lookup (product_id, store_id, forecast_date),
    INDEX idx_forecast_model (model_name, forecast_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

