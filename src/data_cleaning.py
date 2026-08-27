import os
import pandas as pd
import numpy as np


# ============================================================
# 1. PATHS
# ============================================================

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

RAW_PATH = PROJECT_ROOT / "data" / "raw"
PROCESSED_PATH = PROJECT_ROOT / "data" / "processed"

os.makedirs(PROCESSED_PATH, exist_ok=True)


# ============================================================
# 2. LOAD RAW DATA
# ============================================================

ev_maker_place = pd.read_csv(
    os.path.join(RAW_PATH, "EV Maker by Place.csv")
)

ev_category = pd.read_csv(
    os.path.join(RAW_PATH, "ev_cat_01-24.csv")
)

ev_sales = pd.read_csv(
    os.path.join(
        RAW_PATH,
        "ev_sales_by_makers_and_cat_15-24.csv"
    )
)

charging = pd.read_csv(
    os.path.join(RAW_PATH, "OperationalPC.csv")
)

vehicle_class = pd.read_csv(
    os.path.join(RAW_PATH, "Vehicle Class - All.csv")
)


# ============================================================
# 3. CLEAN COLUMN NAMES
# ============================================================

def clean_column_names(df):
    df = df.copy()

    df.columns = (
        df.columns
        .str.strip()
        .str.replace(" ", "_")
        .str.replace("(", "", regex=False)
        .str.replace(")", "", regex=False)
        .str.replace("/", "_")
    )

    return df


ev_maker_place = clean_column_names(ev_maker_place)
ev_category = clean_column_names(ev_category)
ev_sales = clean_column_names(ev_sales)
charging = clean_column_names(charging)
vehicle_class = clean_column_names(vehicle_class)


# ============================================================
# 4. CLEAN TEXT COLUMNS
# ============================================================

def clean_text_columns(df):

    df = df.copy()

    for column in df.select_dtypes(include="object").columns:
        df[column] = (
            df[column]
            .astype(str)
            .str.strip()
        )

        # Convert common missing-value strings to NaN
        df[column] = df[column].replace(
            {
                "": np.nan,
                "nan": np.nan,
                "NA": np.nan,
                "N/A": np.nan,
                "null": np.nan
            }
        )

    return df


ev_maker_place = clean_text_columns(ev_maker_place)
ev_category = clean_text_columns(ev_category)
ev_sales = clean_text_columns(ev_sales)
charging = clean_text_columns(charging)
vehicle_class = clean_text_columns(vehicle_class)


# ============================================================
# 5. CLEAN EV MAKER BY PLACE
# ============================================================

ev_maker_place = ev_maker_place.drop_duplicates()

for column in ["EV_Maker", "Place", "State"]:
    if column in ev_maker_place.columns:
        ev_maker_place[column] = (
            ev_maker_place[column]
            .astype("string")
            .str.strip()
        )


# ============================================================
# 6. CLEAN EV CATEGORY DATA
# ============================================================

ev_category = ev_category.drop_duplicates()

# Convert Date column
if "Date" in ev_category.columns:

    ev_category["Date"] = pd.to_datetime(
        ev_category["Date"],
        errors="coerce"
    )

# Convert all category columns to numeric
category_columns = [
    column
    for column in ev_category.columns
    if column != "Date"
]

for column in category_columns:

    ev_category[column] = pd.to_numeric(
        ev_category[column],
        errors="coerce"
    )

# Missing numeric values represent unavailable values
ev_category[category_columns] = (
    ev_category[category_columns]
    .fillna(0)
)


# ============================================================
# 7. CLEAN EV SALES DATA
# ============================================================

ev_sales = ev_sales.drop_duplicates()

# Clean manufacturer/category names
for column in ["Cat", "Maker"]:

    if column in ev_sales.columns:

        ev_sales[column] = (
            ev_sales[column]
            .astype("string")
            .str.strip()
        )

# Convert yearly sales columns
year_columns = [
    "2015",
    "2016",
    "2017",
    "2018",
    "2019",
    "2020",
    "2021",
    "2022",
    "2023",
    "2024"
]

for year in year_columns:

    if year in ev_sales.columns:

        ev_sales[year] = pd.to_numeric(
            ev_sales[year],
            errors="coerce"
        )

# Missing sales values treated as zero
ev_sales[year_columns] = (
    ev_sales[year_columns]
    .fillna(0)
)

# Create total sales column
ev_sales["Total_Sales_2015_2024"] = (
    ev_sales[year_columns]
    .sum(axis=1)
)


# ============================================================
# 8. CLEAN CHARGING INFRASTRUCTURE
# ============================================================

charging = charging.drop_duplicates()

if "No._of_Operational_PCS" in charging.columns:

    charging["No._of_Operational_PCS"] = (
        pd.to_numeric(
            charging["No._of_Operational_PCS"],
            errors="coerce"
        )
        .fillna(0)
    )


# ============================================================
# 9. CLEAN VEHICLE CLASS DATA
# ============================================================

vehicle_class = vehicle_class.drop_duplicates()

if "Total_Registration" in vehicle_class.columns:

    vehicle_class["Total_Registration"] = (
        pd.to_numeric(
            vehicle_class["Total_Registration"],
            errors="coerce"
        )
        .fillna(0)
    )


# ============================================================
# 10. CREATE YEARLY SALES SUMMARY
# ============================================================

yearly_sales = (
    ev_sales[year_columns]
    .sum()
    .reset_index()
)

yearly_sales.columns = [
    "Year",
    "Total_EV_Sales"
]

yearly_sales["Year"] = (
    yearly_sales["Year"]
    .astype(int)
)

yearly_sales["YoY_Growth_Percent"] = (
    yearly_sales["Total_EV_Sales"]
    .pct_change()
    .mul(100)
)


# ============================================================
# 11. CREATE MANUFACTURER SUMMARY
# ============================================================

manufacturer_summary = (
    ev_sales
    .groupby("Maker", as_index=False)
    ["Total_Sales_2015_2024"]
    .sum()
    .sort_values(
        "Total_Sales_2015_2024",
        ascending=False
    )
)


# ============================================================
# 12. CREATE CATEGORY SUMMARY
# ============================================================

category_summary = (
    ev_sales
    .groupby("Cat", as_index=False)
    ["Total_Sales_2015_2024"]
    .sum()
    .sort_values(
        "Total_Sales_2015_2024",
        ascending=False
    )
)


# ============================================================
# 13. SAVE PROCESSED DATA
# ============================================================

ev_maker_place.to_csv(
    os.path.join(
        PROCESSED_PATH,
        "ev_maker_place_clean.csv"
    ),
    index=False
)

ev_category.to_csv(
    os.path.join(
        PROCESSED_PATH,
        "ev_category_clean.csv"
    ),
    index=False
)

ev_sales.to_csv(
    os.path.join(
        PROCESSED_PATH,
        "ev_sales_clean.csv"
    ),
    index=False
)

charging.to_csv(
    os.path.join(
        PROCESSED_PATH,
        "charging_clean.csv"
    ),
    index=False
)

vehicle_class.to_csv(
    os.path.join(
        PROCESSED_PATH,
        "vehicle_class_clean.csv"
    ),
    index=False
)

yearly_sales.to_csv(
    os.path.join(
        PROCESSED_PATH,
        "yearly_sales_summary.csv"
    ),
    index=False
)

manufacturer_summary.to_csv(
    os.path.join(
        PROCESSED_PATH,
        "manufacturer_summary.csv"
    ),
    index=False
)

category_summary.to_csv(
    os.path.join(
        PROCESSED_PATH,
        "category_summary.csv"
    ),
    index=False
)


# ============================================================
# 14. FINAL VALIDATION
# ============================================================

print("=" * 60)
print("DATA CLEANING COMPLETED")
print("=" * 60)

print("\nProcessed datasets:")

for file in os.listdir(PROCESSED_PATH):
    print(" -", file)

print("\nDataset shapes:")

print(
    "EV Maker:",
    ev_maker_place.shape
)

print(
    "EV Category:",
    ev_category.shape
)

print(
    "EV Sales:",
    ev_sales.shape
)

print(
    "Charging:",
    charging.shape
)

print(
    "Vehicle Class:",
    vehicle_class.shape
)

print("\nYearly sales:")
print(yearly_sales)

print("\nTop 10 manufacturers:")
print(manufacturer_summary.head(10))

print("\nCategory summary:")
print(category_summary)

print("\nCleaning script finished successfully!")