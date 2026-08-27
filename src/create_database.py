from pathlib import Path
import sqlite3
import pandas as pd


# ============================================================
# PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_PATH = PROJECT_ROOT / "data" / "processed"
DATABASE_PATH = PROJECT_ROOT / "ev_market.db"


# ============================================================
# CONNECT TO DATABASE
# ============================================================

connection = sqlite3.connect(DATABASE_PATH)

print("=" * 60)
print("CREATING EV MARKET DATABASE")
print("=" * 60)


# ============================================================
# LOAD CSV FILES
# ============================================================

files = {
    "ev_sales": "ev_sales_clean.csv",
    "ev_category": "ev_category_clean.csv",
    "ev_maker_place": "ev_maker_place_clean.csv",
    "charging": "charging_clean.csv",
    "vehicle_class": "vehicle_class_clean.csv"
}


# ============================================================
# IMPORT DATA INTO SQLITE
# ============================================================

for table_name, file_name in files.items():

    file_path = DATA_PATH / file_name

    df = pd.read_csv(file_path)

    df.to_sql(
        table_name,
        connection,
        if_exists="replace",
        index=False
    )

    print(
        f"{table_name:<20} "
        f"{len(df):>6} rows"
    )


# ============================================================
# VERIFY TABLES
# ============================================================

cursor = connection.cursor()

cursor.execute("""
    SELECT name
    FROM sqlite_master
    WHERE type='table'
    ORDER BY name
""")

tables = cursor.fetchall()

print("\nTables created:")

for table in tables:
    print("-", table[0])


# ============================================================
# CLOSE DATABASE
# ============================================================

connection.close()

print("\nDatabase created successfully!")
print("Location:", DATABASE_PATH)