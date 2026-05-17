select * FROM ecommerce_sales_db.orders_cleaned;


USE ecommerce_sales_db;

CREATE OR REPLACE VIEW vw_kpi_summary AS
SELECT
    SUM(Amount) AS TotalRevenue,
    SUM(Profit) AS TotalProfit,
    SUM(Quantity) AS TotalQuantity
FROM orders_cleaned;

CREATE OR REPLACE VIEW vw_monthly_sales AS
SELECT 
    Year,
    Month,
    Month_Name,
    SUM(Amount) AS MonthlyRevenue
FROM orders_cleaned
GROUP BY Year, Month, Month_Name
ORDER BY Year, Month;


CREATE OR REPLACE VIEW vw_state_sales AS
SELECT 
    State,
    SUM(Amount) AS TotalRevenue,
    SUM(Profit) AS TotalProfit
FROM orders_cleaned
GROUP BY State
ORDER BY TotalRevenue DESC;

CREATE OR REPLACE VIEW vw_category_sales AS
SELECT 
    Category,
    SUM(Amount) AS TotalRevenue,
    SUM(Profit) AS TotalProfit
FROM orders_cleaned
GROUP BY Category
ORDER BY TotalRevenue DESC;

CREATE OR REPLACE VIEW vw_top_customers AS
SELECT 
    CustomerName,
    SUM(Amount) AS Revenue
FROM orders_cleaned
GROUP BY CustomerName
ORDER BY Revenue DESC
LIMIT 10;

CREATE OR REPLACE VIEW vw_subcategory_profitability AS
SELECT 
    Category,
    SubCategory,
    SUM(Amount) AS TotalRevenue,
    SUM(Profit) AS TotalProfit
FROM orders_cleaned
GROUP BY Category, SubCategory
ORDER BY TotalProfit DESC;

CREATE OR REPLACE VIEW vw_north_india_sales AS
SELECT
    State,
    SUM(Amount) AS TotalRevenue,
    SUM(Profit) AS TotalProfit
FROM orders_cleaned
WHERE State IN ('Delhi','Haryana','Punjab','Uttar Pradesh','Uttarakhand','Himachal Pradesh','Jammu & Kashmir','Chandigarh')
GROUP BY State
ORDER BY TotalRevenue DESC;

CREATE OR REPLACE VIEW vw_punjab_weekly_sales AS
SELECT
    YEAR(OrderDate) AS Year,
    WEEK(OrderDate, 3) AS WeekOfYear,
    MIN(OrderDate) AS WeekStart,
    SUM(Amount) AS WeeklyRevenue,
    SUM(Profit) AS WeeklyProfit
FROM orders_cleaned
WHERE State = 'Punjab'
GROUP BY YEAR(OrderDate), WEEK(OrderDate, 3)
ORDER BY Year, WeekOfYear;

CREATE OR REPLACE VIEW vw_top_product_categories AS
SELECT
    Category,
    SUM(Amount) AS TotalRevenue,
    SUM(Profit) AS TotalProfit
FROM orders_cleaned
GROUP BY Category
ORDER BY TotalRevenue DESC
LIMIT 10;


