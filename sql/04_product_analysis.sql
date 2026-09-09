-- 04 Product Analysis

WITH product_sales AS (
    SELECT
        stock_code,
        MAX(description) AS description,
        SUM(quantity) AS total_quantity,
        SUM(quantity * price) AS total_revenue
    FROM retail_transactions_raw
    WHERE invoice NOT LIKE 'C%'
      AND quantity > 0
      AND price > 0
      AND stock_code NOT IN ('M', 'DOT', 'POST')
    GROUP BY stock_code
)
SELECT
    stock_code,
    description,
    total_quantity,
    ROUND(total_revenue, 2) AS total_revenue,
    ROUND(
        100.0 * total_revenue
        / SUM(total_revenue) OVER (),
        2
    ) AS revenue_share_pct
FROM product_sales
ORDER BY total_revenue DESC
LIMIT 20;
