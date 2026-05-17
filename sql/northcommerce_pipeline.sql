-- northcommerce_pipeline.sql
-- Production-ready CTE chain for enriched orders, weekly aggregations, anomalies, RFM, and CLV estimates

-- Note: Adapt date functions to your RDBMS if needed (this SQL targets MySQL/compatible dialect)

CREATE OR REPLACE VIEW v_orders_enriched AS
SELECT
  o.`Order ID` AS order_id,
  PARSE_DATE('%Y-%m-%d', o.`Order Date`) AS order_date,
  o.CustomerName AS customer_name,
  o.State,
  o.City,
  o.Category,
  o.`Sub-Category` AS sub_category,
  o.Amount AS amount,
  o.Profit AS profit,
  o.Quantity AS quantity,
  p.product_sku,
  c.customer_id,
  -- flags
  CASE WHEN o.State IN ('Delhi','Haryana','Punjab','Uttar Pradesh','Uttarakhand','Himachal Pradesh','Jammu & Kashmir','Chandigarh') THEN 1 ELSE 0 END AS is_north_india
FROM orders_cleaned o
LEFT JOIN products p ON TRIM(o.`Sub-Category`) = p.category_name -- example join
LEFT JOIN customers c ON o.CustomerName = c.customer_name;

-- weekly per-region aggregation
CREATE OR REPLACE VIEW v_weekly_region AS
WITH base AS (
  SELECT
    DATE_TRUNC('week', order_date) AS week_start,
    State,
    SUM(amount) AS total_revenue,
    SUM(profit) AS total_profit,
    SUM(quantity) as total_qty,
    COUNT(DISTINCT order_id) as orders_count
  FROM v_orders_enriched
  GROUP BY DATE_TRUNC('week', order_date), State
)
SELECT * FROM base;

-- Week-over-week change + rolling
CREATE OR REPLACE VIEW v_weekly_wow AS
WITH w AS (
  SELECT
    week_start,
    State,
    total_revenue,
    LAG(total_revenue) OVER (PARTITION BY State ORDER BY week_start) AS prev_revenue,
    AVG(total_revenue) OVER (PARTITION BY State ORDER BY week_start ROWS BETWEEN 3 PRECEDING AND CURRENT ROW) AS rolling_4wk_avg,
    STDDEV_SAMP(total_revenue) OVER (PARTITION BY State ORDER BY week_start ROWS BETWEEN 3 PRECEDING AND CURRENT ROW) AS rolling_4wk_std
  FROM v_weekly_region
)
SELECT
  week_start,
  State,
  total_revenue,
  prev_revenue,
  CASE WHEN prev_revenue IS NULL THEN NULL ELSE (total_revenue - prev_revenue) / prev_revenue END AS wow_pct,
  rolling_4wk_avg,
  rolling_4wk_std
FROM w;

-- anomaly flags using z-score severity
CREATE OR REPLACE VIEW v_anomaly_flags AS
SELECT
  w.*,
  CASE
    WHEN rolling_4wk_std IS NULL THEN 'normal'
    WHEN (total_revenue - rolling_4wk_avg) / NULLIF(rolling_4wk_std,0) >= 2.5 THEN 'critical'
    WHEN (total_revenue - rolling_4wk_avg) / NULLIF(rolling_4wk_std,0) >= 1.5 THEN 'warning'
    WHEN (total_revenue - rolling_4wk_avg) / NULLIF(rolling_4wk_std,0) >= 1.0 THEN 'watch'
    ELSE 'normal'
  END AS severity,
  CASE WHEN total_revenue - rolling_4wk_avg < 0 THEN 'down' ELSE 'up' END AS direction
FROM v_weekly_wow w;

-- city weekly drilldown for Punjab root cause
CREATE OR REPLACE VIEW v_city_weekly AS
SELECT
  DATE_TRUNC('week', order_date) AS week_start,
  City,
  SUM(amount) AS weekly_revenue,
  SUM(profit) AS weekly_profit,
  COUNT(DISTINCT order_id) AS weekly_orders
FROM v_orders_enriched
WHERE State = 'Punjab'
GROUP BY DATE_TRUNC('week', order_date), City;

-- RFM scores: quintile-based
CREATE OR REPLACE VIEW v_rfm_scores AS
WITH last_order AS (
  SELECT customer_name, MAX(order_date) AS last_order_date
  FROM v_orders_enriched GROUP BY customer_name
),
metrics AS (
  SELECT
    r.customer_name,
    DATEDIFF(CURRENT_DATE, lo.last_order_date) AS recency,
    COUNT(DISTINCT r.order_id) AS frequency,
    SUM(r.amount) AS monetary
  FROM v_orders_enriched r
  LEFT JOIN last_order lo ON r.customer_name = lo.customer_name
  GROUP BY r.customer_name, lo.last_order_date
)
SELECT
  customer_name,
  recency,
  frequency,
  monetary,
  NTILE(5) OVER (ORDER BY recency) AS r_quintile_rev,
  NTILE(5) OVER (ORDER BY frequency) AS f_quintile_rev,
  NTILE(5) OVER (ORDER BY monetary) AS m_quintile_rev
FROM metrics;

-- simplified CLV estimate using average order value * expected purchases (placeholder for BG/NBD integration)
CREATE OR REPLACE VIEW v_clv_estimate AS
SELECT
  customer_name,
  monetary AS lifetime_value_approx,
  (monetary / NULLIF(frequency,0)) AS avg_order_value
FROM (
  SELECT customer_name, SUM(monetary) AS monetary, SUM(frequency) AS frequency
  FROM (
    SELECT customer_name, amount AS monetary, 1 AS frequency FROM v_orders_enriched
  ) t
  GROUP BY customer_name
) s;

-- Power BI ready flattened views
CREATE OR REPLACE VIEW v_pbi_weekly_region AS
SELECT week_start, State, total_revenue, total_profit, total_qty, orders_count FROM v_weekly_region;

CREATE OR REPLACE VIEW v_pbi_city_punjab AS
SELECT * FROM v_city_weekly;

CREATE OR REPLACE VIEW v_pbi_rfm AS
SELECT * FROM v_rfm_scores;

-- End of file
