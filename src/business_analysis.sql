-- ============================================================
-- EV MARKET BUSINESS ANALYSIS
-- ============================================================


-- ============================================================
-- 1. CHECK TABLES
-- ============================================================

SELECT name
FROM sqlite_master
WHERE type = 'table';


-- ============================================================
-- 2. TOTAL SALES BY YEAR
-- ============================================================

SELECT
    SUM("2015") AS sales_2015,
    SUM("2016") AS sales_2016,
    SUM("2017") AS sales_2017,
    SUM("2018") AS sales_2018,
    SUM("2019") AS sales_2019,
    SUM("2020") AS sales_2020,
    SUM("2021") AS sales_2021,
    SUM("2022") AS sales_2022,
    SUM("2023") AS sales_2023,
    SUM("2024") AS sales_2024
FROM ev_sales;


-- ============================================================
-- 3. TOP MANUFACTURERS
-- ============================================================

SELECT
    Maker,
    SUM(Total_Sales_2015_2024) AS total_sales
FROM ev_sales
GROUP BY Maker
ORDER BY total_sales DESC
LIMIT 15;


-- ============================================================
-- 4. MANUFACTURER MARKET SHARE
-- ============================================================

SELECT
    Maker,
    SUM(Total_Sales_2015_2024) AS total_sales,

    ROUND(
        SUM(Total_Sales_2015_2024) * 100.0 /
        (
            SELECT SUM(Total_Sales_2015_2024)
            FROM ev_sales
        ),
        2
    ) AS market_share_percent

FROM ev_sales

GROUP BY Maker

ORDER BY total_sales DESC;


-- ============================================================
-- 5. CATEGORY PERFORMANCE
-- ============================================================

SELECT
    Cat,
    SUM(Total_Sales_2015_2024) AS total_sales
FROM ev_sales
GROUP BY Cat
ORDER BY total_sales DESC;


-- ============================================================
-- 6. CATEGORY MARKET SHARE
-- ============================================================

SELECT
    Cat,

    SUM(Total_Sales_2015_2024) AS total_sales,

    ROUND(
        SUM(Total_Sales_2015_2024) * 100.0 /
        (
            SELECT SUM(Total_Sales_2015_2024)
            FROM ev_sales
        ),
        2
    ) AS market_share_percent

FROM ev_sales

GROUP BY Cat

ORDER BY total_sales DESC;


-- ============================================================
-- 7. CHARGING INFRASTRUCTURE BY STATE
-- ============================================================

SELECT
    State,
    "No._of_Operational_PCS" AS operational_charging_points
FROM charging
ORDER BY operational_charging_points DESC;


-- ============================================================
-- 8. TOTAL CHARGING INFRASTRUCTURE
-- ============================================================

SELECT
    SUM("No._of_Operational_PCS")
    AS total_operational_charging_points
FROM charging;


-- ============================================================
-- 9. EV MANUFACTURERS BY STATE
-- ============================================================

SELECT
    State,
    COUNT(DISTINCT EV_Maker)
    AS number_of_manufacturers
FROM ev_maker_place
GROUP BY State
ORDER BY number_of_manufacturers DESC;


-- ============================================================
-- 10. MANUFACTURER + CATEGORY PERFORMANCE
-- ============================================================

SELECT
    Cat,
    Maker,
    SUM(Total_Sales_2015_2024) AS total_sales
FROM ev_sales
GROUP BY Cat, Maker
ORDER BY Cat, total_sales DESC;


-- ============================================================
-- 11. TOP MANUFACTURER IN EACH CATEGORY
-- ============================================================

WITH manufacturer_category AS (

    SELECT
        Cat,
        Maker,
        SUM(Total_Sales_2015_2024) AS total_sales

    FROM ev_sales

    GROUP BY Cat, Maker
),

ranked AS (

    SELECT
        Cat,
        Maker,
        total_sales,

        RANK() OVER (
            PARTITION BY Cat
            ORDER BY total_sales DESC
        ) AS category_rank

    FROM manufacturer_category
)

SELECT
    Cat,
    Maker,
    total_sales
FROM ranked
WHERE category_rank = 1
ORDER BY total_sales DESC;


-- ============================================================
-- 12. MANUFACTURER PERFORMANCE 2023 vs 2024
-- ============================================================

SELECT
    Maker,

    SUM("2023") AS sales_2023,

    SUM("2024") AS sales_2024,

    ROUND(
        (
            SUM("2024") -
            SUM("2023")
        ) * 100.0 /
        NULLIF(SUM("2023"), 0),
        2
    ) AS growth_percent

FROM ev_sales

GROUP BY Maker

HAVING SUM("2023") > 0

ORDER BY growth_percent DESC;


-- ============================================================
-- 13. CHARGING INFRASTRUCTURE RANK
-- ============================================================

SELECT
    State,
    "No._of_Operational_PCS" AS charging_points,

    RANK() OVER (
        ORDER BY "No._of_Operational_PCS" DESC
    ) AS infrastructure_rank

FROM charging

ORDER BY infrastructure_rank;


-- ============================================================
-- 14. VEHICLE CLASS RANKING
-- ============================================================

SELECT
    Vehicle_Class,
    Total_Registration,

    RANK() OVER (
        ORDER BY Total_Registration DESC
    ) AS registration_rank

FROM vehicle_class

ORDER BY registration_rank;


-- ============================================================
-- 15. TOP 5 MANUFACTURER CONCENTRATION
-- ============================================================

WITH manufacturer_sales AS (

    SELECT
        Maker,
        SUM(Total_Sales_2015_2024) AS sales

    FROM ev_sales

    GROUP BY Maker
),

ranked AS (

    SELECT
        Maker,
        sales,

        RANK() OVER (
            ORDER BY sales DESC
        ) AS ranking

    FROM manufacturer_sales
)

SELECT
    SUM(sales) AS top_5_sales,

    ROUND(
        SUM(sales) * 100.0 /
        (
            SELECT SUM(sales)
            FROM manufacturer_sales
        ),
        2
    ) AS top_5_market_share

FROM ranked

WHERE ranking <= 5;