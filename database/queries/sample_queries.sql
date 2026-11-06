-- ==============================================================================
-- ShopCast - Baseline Analytical Queries for Sales & Forecast Evaluation
-- ==============================================================================

-- 1. Daily Sales Summary by Category
SELECT 
    s.transaction_date,
    p.category,
    COUNT(DISTINCT s.transaction_id) AS total_transactions,
    SUM(s.quantity) AS total_units_sold,
    SUM(s.total_amount) AS total_revenue
FROM fact_sales s
JOIN dim_products p ON s.product_id = p.product_id
GROUP BY s.transaction_date, p.category
ORDER BY s.transaction_date DESC, total_revenue DESC;

-- 2. Top 10 Selling Products over Last 30 Days
SELECT 
    p.sku,
    p.product_name,
    p.category,
    SUM(s.quantity) AS units_sold,
    SUM(s.total_amount) AS revenue
FROM fact_sales s
JOIN dim_products p ON s.product_id = p.product_id
WHERE s.transaction_date >= CURDATE() - INTERVAL 30 DAY
GROUP BY p.product_id, p.sku, p.product_name, p.category
ORDER BY revenue DESC
LIMIT 10;

-- 3. Actual vs Predicted Forecast Comparison (Evaluation Query)
SELECT 
    f.forecast_date,
    p.product_name,
    f.model_name,
    COALESCE(s.quantity, 0) AS actual_quantity,
    f.predicted_quantity,
    f.lower_bound,
    f.upper_bound,
    (f.predicted_quantity - COALESCE(s.quantity, 0)) AS forecast_error
FROM fact_forecasts f
JOIN dim_products p ON f.product_id = p.product_id
LEFT JOIN (
    SELECT transaction_date, product_id, SUM(quantity) AS quantity
    FROM fact_sales
    GROUP BY transaction_date, product_id
) s ON f.forecast_date = s.transaction_date AND f.product_id = s.product_id
ORDER BY f.forecast_date DESC;

