-- 02 Sales Analysis

SELECT
    DATE_TRUNC('month', invoice_date) AS month,
    SUM(quantity * price) AS monthly_revenue,
    COUNT(DISTINCT invoice) AS monthly_orders,
    ROUND(
        SUM(quantity * price)
        / COUNT(DISTINCT invoice),
        2
    ) AS aov
FROM retail_transactions_raw
WHERE invoice NOT LIKE 'C%'
GROUP BY DATE_TRUNC('month', invoice_date)
ORDER BY month;
