-- 03 Customer RFM Analysis

WITH customer_rfm AS (
    SELECT
        customer_id,
        DATE '2011-12-09' - MAX(invoice_date)::DATE AS recency_days,
        COUNT(DISTINCT invoice) AS total_orders,
        SUM(quantity * price) AS customer_revenue
    FROM retail_transactions_raw
    WHERE invoice NOT LIKE 'C%'
      AND customer_id IS NOT NULL
    GROUP BY customer_id
),
rfm_scores AS (
    SELECT
        customer_id,
        recency_days,
        total_orders,
        customer_revenue,
        NTILE(5) OVER (ORDER BY recency_days DESC) AS r_score,
        NTILE(5) OVER (ORDER BY total_orders) AS f_score,
        NTILE(5) OVER (ORDER BY customer_revenue) AS m_score
    FROM customer_rfm
),
rfm_final AS (
    SELECT
        *,
        CASE
            WHEN r_score >= 4 AND f_score >= 4 AND m_score >= 4 THEN 'Champions'
            WHEN r_score >= 3 AND f_score >= 4 AND m_score >= 3 THEN 'Loyal Customers'
            WHEN r_score >= 4 AND m_score >= 4 AND f_score < 4 THEN 'Big Spenders'
            WHEN r_score <= 2 AND f_score >= 3 AND m_score >= 3 THEN 'At Risk'
            WHEN r_score <= 2 AND f_score <= 2 THEN 'Lost Customers'
            ELSE 'Others'
        END AS customer_segment
    FROM rfm_scores
)
SELECT
    customer_segment,
    COUNT(*) AS customer_count,
    ROUND(SUM(customer_revenue), 2) AS total_revenue,
    ROUND(
        100.0 * SUM(customer_revenue)
        / SUM(SUM(customer_revenue)) OVER (),
        2
    ) AS revenue_share_pct,
    ROUND(AVG(customer_revenue), 2) AS avg_customer_revenue,
    ROUND(AVG(total_orders), 2) AS avg_orders
FROM rfm_final
GROUP BY customer_segment
ORDER BY total_revenue DESC;
