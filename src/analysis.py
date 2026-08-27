from pathlib import Path

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# ============================================================
# 1. PROJECT PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

PROCESSED_PATH = PROJECT_ROOT / "data" / "processed"
REPORT_PATH = PROJECT_ROOT / "reports"

FIGURE_PATH = REPORT_PATH / "screenshots"

FIGURE_PATH.mkdir(parents=True, exist_ok=True)


# ============================================================
# 2. LOAD CLEAN DATA
# ============================================================

ev_maker_place = pd.read_csv(
    PROCESSED_PATH / "ev_maker_place_clean.csv"
)

ev_category = pd.read_csv(
    PROCESSED_PATH / "ev_category_clean.csv"
)

ev_sales = pd.read_csv(
    PROCESSED_PATH / "ev_sales_clean.csv"
)

charging = pd.read_csv(
    PROCESSED_PATH / "charging_clean.csv"
)

vehicle_class = pd.read_csv(
    PROCESSED_PATH / "vehicle_class_clean.csv"
)


# ============================================================
# 3. BASIC INFORMATION
# ============================================================

print("=" * 70)
print("EV MARKET & BUSINESS ANALYTICS")
print("PYTHON BUSINESS ANALYSIS")
print("=" * 70)

print("\nDataset sizes:")

print("EV Maker by Place:", ev_maker_place.shape)
print("EV Category:", ev_category.shape)
print("EV Sales:", ev_sales.shape)
print("Charging:", charging.shape)
print("Vehicle Class:", vehicle_class.shape)


# ============================================================
# 4. YEARLY EV SALES ANALYSIS
# ============================================================

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

yearly_sales = (
    ev_sales[year_columns]
    .sum()
)

yearly_sales_df = (
    yearly_sales
    .reset_index()
)

yearly_sales_df.columns = [
    "Year",
    "Total_EV_Sales"
]

yearly_sales_df["Year"] = (
    yearly_sales_df["Year"]
    .astype(int)
)


# ============================================================
# 5. YEAR-OVER-YEAR GROWTH
# ============================================================

yearly_sales_df["YoY_Growth_Percent"] = (
    yearly_sales_df["Total_EV_Sales"]
    .pct_change()
    .mul(100)
)


print("\n")
print("=" * 70)
print("YEARLY EV SALES")
print("=" * 70)

print(yearly_sales_df.to_string(index=False))


# ============================================================
# 6. MARKET GROWTH CHART
# ============================================================

plt.figure(figsize=(12, 6))

plt.plot(
    yearly_sales_df["Year"],
    yearly_sales_df["Total_EV_Sales"],
    marker="o"
)

plt.title("India EV Sales Trend (2015–2024)")
plt.xlabel("Year")
plt.ylabel("Total EV Sales")

plt.xticks(
    yearly_sales_df["Year"]
)

plt.tight_layout()

plt.savefig(
    FIGURE_PATH / "01_ev_sales_trend.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()


# ============================================================
# 7. YOY GROWTH CHART
# ============================================================

plt.figure(figsize=(12, 6))

plt.bar(
    yearly_sales_df["Year"],
    yearly_sales_df["YoY_Growth_Percent"]
)

plt.axhline(
    y=0,
    linewidth=1
)

plt.title("Year-over-Year EV Sales Growth")
plt.xlabel("Year")
plt.ylabel("YoY Growth (%)")

plt.xticks(
    yearly_sales_df["Year"]
)

plt.tight_layout()

plt.savefig(
    FIGURE_PATH / "02_yoy_growth.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()


# ============================================================
# 8. TOTAL MARKET SALES
# ============================================================

total_market_sales = (
    ev_sales["Total_Sales_2015_2024"]
    .sum()
)

print("\nTotal EV sales from 2015–2024:")
print(f"{total_market_sales:,.0f}")


# ============================================================
# 9. MANUFACTURER ANALYSIS
# ============================================================

manufacturer_sales = (
    ev_sales
    .groupby("Maker")["Total_Sales_2015_2024"]
    .sum()
    .sort_values(ascending=False)
)

print("\n")
print("=" * 70)
print("TOP 15 EV MANUFACTURERS")
print("=" * 70)

print(
    manufacturer_sales
    .head(15)
    .to_string()
)


# ============================================================
# 10. MANUFACTURER MARKET SHARE
# ============================================================

manufacturer_share = (
    manufacturer_sales
    / total_market_sales
    * 100
)

manufacturer_share = (
    manufacturer_share
    .sort_values(ascending=False)
)

print("\n")
print("=" * 70)
print("TOP MANUFACTURERS BY MARKET SHARE")
print("=" * 70)

print(
    manufacturer_share
    .head(15)
    .round(2)
    .to_string()
)


# ============================================================
# 11. TOP MANUFACTURERS CHART
# ============================================================

top_manufacturers = (
    manufacturer_sales
    .head(15)
    .sort_values()
)

plt.figure(figsize=(12, 8))

plt.barh(
    top_manufacturers.index,
    top_manufacturers.values
)

plt.title(
    "Top EV Manufacturers by Total Sales (2015–2024)"
)

plt.xlabel("Total EV Sales")
plt.ylabel("Manufacturer")

plt.tight_layout()

plt.savefig(
    FIGURE_PATH / "03_top_manufacturers.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()


# ============================================================
# 12. CATEGORY ANALYSIS
# ============================================================

category_sales = (
    ev_sales
    .groupby("Cat")["Total_Sales_2015_2024"]
    .sum()
    .sort_values(ascending=False)
)

category_share = (
    category_sales
    / total_market_sales
    * 100
)

print("\n")
print("=" * 70)
print("EV CATEGORY ANALYSIS")
print("=" * 70)

category_summary = pd.DataFrame({
    "Total_Sales": category_sales,
    "Market_Share_Percent": category_share
})

print(
    category_summary
    .round(2)
    .to_string()
)


# ============================================================
# 13. CATEGORY CHART
# ============================================================

plt.figure(figsize=(12, 7))

category_sales.sort_values().plot(
    kind="barh"
)

plt.title(
    "EV Sales by Vehicle Category (2015–2024)"
)

plt.xlabel("Total EV Sales")
plt.ylabel("Vehicle Category")

plt.tight_layout()

plt.savefig(
    FIGURE_PATH / "04_category_sales.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()


# ============================================================
# 14. STATE / MANUFACTURER LOCATION ANALYSIS
# ============================================================

makers_by_state = (
    ev_maker_place
    .groupby("State")["EV_Maker"]
    .nunique()
    .sort_values(ascending=False)
)

print("\n")
print("=" * 70)
print("EV MANUFACTURERS BY STATE")
print("=" * 70)

print(
    makers_by_state
    .to_string()
)


# ============================================================
# 15. MANUFACTURER LOCATION CHART
# ============================================================

top_maker_states = (
    makers_by_state
    .head(15)
    .sort_values()
)

plt.figure(figsize=(12, 7))

plt.barh(
    top_maker_states.index,
    top_maker_states.values
)

plt.title(
    "Top States by Number of EV Manufacturers"
)

plt.xlabel("Number of EV Manufacturers")
plt.ylabel("State")

plt.tight_layout()

plt.savefig(
    FIGURE_PATH / "05_manufacturers_by_state.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()


# ============================================================
# 16. CHARGING INFRASTRUCTURE ANALYSIS
# ============================================================

charging = charging.sort_values(
    "No._of_Operational_PCS",
    ascending=False
)

total_charging_points = (
    charging["No._of_Operational_PCS"]
    .sum()
)

print("\n")
print("=" * 70)
print("CHARGING INFRASTRUCTURE")
print("=" * 70)

print(
    "\nTotal operational charging points:",
    f"{total_charging_points:,.0f}"
)

print("\nTop states:")

print(
    charging
    .head(15)
    .to_string(index=False)
)


# ============================================================
# 17. CHARGING INFRASTRUCTURE CHART
# ============================================================

top_charging_states = (
    charging
    .head(15)
    .sort_values(
        "No._of_Operational_PCS"
    )
)

plt.figure(figsize=(12, 7))

plt.barh(
    top_charging_states["State"],
    top_charging_states["No._of_Operational_PCS"]
)

plt.title(
    "Top States by Operational EV Charging Points"
)

plt.xlabel("Operational Charging Points")
plt.ylabel("State")

plt.tight_layout()

plt.savefig(
    FIGURE_PATH / "06_charging_infrastructure.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()


# ============================================================
# 18. VEHICLE CLASS ANALYSIS
# ============================================================

vehicle_class = vehicle_class.sort_values(
    "Total_Registration",
    ascending=False
)

print("\n")
print("=" * 70)
print("VEHICLE CLASS REGISTRATIONS")
print("=" * 70)

print(
    vehicle_class
    .to_string(index=False)
)


# ============================================================
# 19. VEHICLE CLASS CHART
# ============================================================

plt.figure(figsize=(12, 7))

plt.barh(
    vehicle_class["Vehicle_Class"],
    vehicle_class["Total_Registration"]
)

plt.title(
    "Vehicle Registrations by Vehicle Class"
)

plt.xlabel("Total Registration")
plt.ylabel("Vehicle Class")

plt.tight_layout()

plt.savefig(
    FIGURE_PATH / "07_vehicle_class.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()


# ============================================================
# 20. KEY BUSINESS FINDINGS
# ============================================================

top_manufacturer = manufacturer_sales.index[0]
top_category = category_sales.index[0]
top_manufacturer_state = makers_by_state.index[0]
top_charging_state = charging.iloc[0]["State"]

best_growth_year = (
    yearly_sales_df
    .dropna(subset=["YoY_Growth_Percent"])
    .sort_values(
        "YoY_Growth_Percent",
        ascending=False
    )
    .iloc[0]
)


print("\n")
print("=" * 70)
print("KEY BUSINESS FINDINGS")
print("=" * 70)

print(
    f"\n1. Highest-selling manufacturer: "
    f"{top_manufacturer}"
)

print(
    f"\n2. Largest vehicle category: "
    f"{top_category}"
)

print(
    f"\n3. State with most EV manufacturers: "
    f"{top_manufacturer_state}"
)

print(
    f"\n4. State with most operational charging points: "
    f"{top_charging_state}"
)

print(
    f"\n5. Highest YoY growth occurred in: "
    f"{int(best_growth_year['Year'])}"
)

print(
    f"   Growth: "
    f"{best_growth_year['YoY_Growth_Percent']:.2f}%"
)


# ============================================================
# 21. SAVE ANALYTICAL OUTPUTS
# ============================================================

yearly_sales_df.to_csv(
    PROCESSED_PATH / "yearly_sales_analysis.csv",
    index=False
)

manufacturer_summary = pd.DataFrame({
    "Manufacturer": manufacturer_sales.index,
    "Total_Sales_2015_2024": manufacturer_sales.values,
    "Market_Share_Percent": manufacturer_share[
        manufacturer_sales.index
    ].values
})

manufacturer_summary.to_csv(
    PROCESSED_PATH / "manufacturer_analysis.csv",
    index=False
)

category_summary = category_summary.reset_index()

category_summary.columns = [
    "Category",
    "Total_Sales",
    "Market_Share_Percent"
]

category_summary.to_csv(
    PROCESSED_PATH / "category_analysis.csv",
    index=False
)


print("\n")
print("=" * 70)
print("ANALYSIS COMPLETED SUCCESSFULLY")
print("=" * 70)

print(
    "\nCharts saved to:",
    FIGURE_PATH
)

print(
    "\nAnalysis files saved to:",
    PROCESSED_PATH
)