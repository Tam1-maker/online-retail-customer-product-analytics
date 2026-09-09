-- 01 Data Overview

SELECT
    COUNT(*) AS total_rows,
    COUNT(DISTINCT invoice) AS total_invoices,
    COUNT(DISTINCT stock_code) AS total_products,
    COUNT(DISTINCT customer_id) AS total_customers,
    COUNT(DISTINCT country) AS total_countries
FROM retail_transactions_raw;

SELECT
    SUM(quantity * price) AS total_revenue
FROM retail_transactions_raw
WHERE invoice NOT LIKE 'C%';

SELECT
    COUNT(*) AS cancelled_lines,
    SUM(quantity * price) AS cancelled_amount
FROM retail_transactions_raw
WHERE invoice LIKE 'C%';
