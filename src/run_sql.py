from pathlib import Path
import sqlite3
import pandas as pd


# ============================================================
# PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATABASE_PATH = PROJECT_ROOT / "ev_market.db"
SQL_PATH = PROJECT_ROOT / "sql" / "business_analysis.sql"

OUTPUT_PATH = PROJECT_ROOT / "data" / "processed" / "sql_results"

OUTPUT_PATH.mkdir(parents=True, exist_ok=True)


# ============================================================
# CONNECT TO DATABASE
# ============================================================

connection = sqlite3.connect(DATABASE_PATH)

print("=" * 70)
print("EV MARKET SQL BUSINESS ANALYSIS")
print("=" * 70)


# ============================================================
# CHECK TABLES
# ============================================================

tables = pd.read_sql_query(
    """
    SELECT name
    FROM sqlite_master
    WHERE type = 'table'
    ORDER BY name
    """,
    connection
)

print("\nDATABASE TABLES:")
print(tables.to_string(index=False))


# ============================================================
# BUSINESS QUERY 1
# TOP MANUFACTURERS
# ============================================================

query = """
SELECT
    Maker,
    SUM(Total_Sales_2015_2024) AS total_sales
FROM ev_sales
GROUP BY Maker
ORDER BY total_sales DESC
LIMIT 15;
"""

top_manufacturers = pd.read_sql_query(
    query,
    connection
)

print("\n" + "=" * 70)
print("TOP 15 EV MANUFACTURERS")
print("=" * 70)

print(
    top_manufacturers
    .to_string(index=False)
)

top_manufacturers.to_csv(
    OUTPUT_PATH / "top_manufacturers.csv",
    index=False
)


# ============================================================
# BUSINESS QUERY 2
# MANUFACTURER MARKET SHARE
# ============================================================

query = """
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
"""

market_share = pd.read_sql_query(
    query,
    connection
)

print("\n" + "=" * 70)
print("MANUFACTURER MARKET SHARE")
print("=" * 70)

print(
    market_share.head(15)
    .to_string(index=False)
)

market_share.to_csv(
    OUTPUT_PATH / "manufacturer_market_share.csv",
    index=False
)


# ============================================================
# BUSINESS QUERY 3
# CATEGORY PERFORMANCE
# ============================================================

query = """
SELECT
    Cat,
    SUM(Total_Sales_2015_2024) AS total_sales
FROM ev_sales
GROUP BY Cat
ORDER BY total_sales DESC;
"""

category_performance = pd.read_sql_query(
    query,
    connection
)

print("\n" + "=" * 70)
print("CATEGORY PERFORMANCE")
print("=" * 70)

print(
    category_performance
    .to_string(index=False)
)

category_performance.to_csv(
    OUTPUT_PATH / "category_performance.csv",
    index=False
)


# ============================================================
# BUSINESS QUERY 4
# CHARGING INFRASTRUCTURE
# ============================================================

query = """
SELECT
    State,
    "No._of_Operational_PCS" AS operational_charging_points
FROM charging
ORDER BY operational_charging_points DESC;
"""

charging_analysis = pd.read_sql_query(
    query,
    connection
)

print("\n" + "=" * 70)
print("CHARGING INFRASTRUCTURE")
print("=" * 70)

print(
    charging_analysis
    .head(15)
    .to_string(index=False)
)

charging_analysis.to_csv(
    OUTPUT_PATH / "charging_analysis.csv",
    index=False
)


# ============================================================
# BUSINESS QUERY 5
# EV MANUFACTURERS BY STATE
# ============================================================

query = """
SELECT
    State,
    COUNT(DISTINCT EV_Maker) AS number_of_manufacturers
FROM ev_maker_place
GROUP BY State
ORDER BY number_of_manufacturers DESC;
"""

state_manufacturers = pd.read_sql_query(
    query,
    connection
)

print("\n" + "=" * 70)
print("EV MANUFACTURERS BY STATE")
print("=" * 70)

print(
    state_manufacturers
    .to_string(index=False)
)

state_manufacturers.to_csv(
    OUTPUT_PATH / "manufacturers_by_state.csv",
    index=False
)


# ============================================================
# BUSINESS QUERY 6
# 2023 → 2024 GROWTH
# ============================================================

query = """
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
"""

growth_analysis = pd.read_sql_query(
    query,
    connection
)

print("\n" + "=" * 70)
print("2023 → 2024 MANUFACTURER GROWTH")
print("=" * 70)

print(
    growth_analysis
    .head(15)
    .to_string(index=False)
)

growth_analysis.to_csv(
    OUTPUT_PATH / "manufacturer_growth.csv",
    index=False
)


# ============================================================
# BUSINESS QUERY 7
# TOP MANUFACTURER IN EACH CATEGORY
# ============================================================

query = """
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
"""

category_leaders = pd.read_sql_query(
    query,
    connection
)

print("\n" + "=" * 70)
print("CATEGORY LEADERS")
print("=" * 70)

print(
    category_leaders
    .to_string(index=False)
)

category_leaders.to_csv(
    OUTPUT_PATH / "category_leaders.csv",
    index=False
)


# ============================================================
# CLOSE DATABASE
# ============================================================

connection.close()


print("\n" + "=" * 70)
print("SQL ANALYSIS COMPLETED")
print("=" * 70)

print("\nResults saved to:")

for file in OUTPUT_PATH.iterdir():
    print("-", file.name)