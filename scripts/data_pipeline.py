import os
from pathlib import Path

import pandas as pd

NORTH_INDIA_STATES = [
    "Delhi",
    "Haryana",
    "Punjab",
    "Uttar Pradesh",
    "Uttarakhand",
    "Himachal Pradesh",
    "Jammu & Kashmir",
    "Chandigarh",
]


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def load_raw_orders() -> pd.DataFrame:
    raw_path = repo_root() / "data" / "merged_orders.csv"
    if not raw_path.exists():
        raise FileNotFoundError(f"Expected raw data at {raw_path}")
    df = pd.read_csv(raw_path)
    return df


def clean_orders(df: pd.DataFrame) -> pd.DataFrame:
    df["Order Date"] = pd.to_datetime(df["Order Date"], format="%d-%m-%Y", errors="coerce")
    df = df.dropna(subset=["Order Date"])
    df["Year"] = df["Order Date"].dt.year
    df["Month"] = df["Order Date"].dt.month
    df["Month_Name"] = df["Order Date"].dt.strftime("%b")
    df["Quarter"] = df["Order Date"].dt.quarter
    df["Order Week"] = df["Order Date"].dt.to_period("W").apply(lambda p: p.start_time)
    df["North India"] = df["State"].isin(NORTH_INDIA_STATES)
    return df


def save_clean_file(df: pd.DataFrame):
    data_dir = repo_root() / "data"
    cleaned_path = data_dir / "merged_orders_cleaned.csv"
    df.to_csv(cleaned_path, index=False)
    print(f"Saved cleaned data to {cleaned_path}")


def export_summary_files(df: pd.DataFrame):
    output_dir = repo_root() / "outputs"
    output_dir.mkdir(exist_ok=True)

    total_orders = df["Order ID"].nunique()
    total_amount = df["Amount"].sum()
    kpi_summary = {
        "Total Revenue": total_amount,
        "Total Orders": total_orders,
        "Unique Customers": df["CustomerName"].nunique(),
        "Average Order Value": total_amount / total_orders if total_orders else 0,
        "North India Revenue Share": df.loc[df["North India"], "Amount"].sum() / total_amount if total_amount else 0,
    }
    pd.DataFrame.from_dict(kpi_summary, orient="index", columns=["Value"]).to_csv(
        output_dir / "kpi_summary.csv"
    )

    weekly_sales = (
        df.groupby(["Order Week", "North India"])["Amount"].sum().reset_index()
        .sort_values(["Order Week", "North India"], ascending=[True, False])
    )
    weekly_sales.to_csv(output_dir / "weekly_sales_north_india.csv", index=False)

    north_region = (
        df[df["North India"]].groupby(["State"])[["Amount", "Profit"]].sum().reset_index().sort_values("Amount", ascending=False)
    )
    north_region.to_csv(output_dir / "north_india_state_sales.csv", index=False)

    punjab_trends = (
        df[df["State"] == "Punjab"].groupby(["Order Week"])[["Amount", "Profit"]].sum().reset_index().sort_values("Order Week")
    )
    punjab_trends.to_csv(output_dir / "punjab_weekly_trends.csv", index=False)

    top_products = (
        df.groupby(["Category", "Sub-Category"])["Amount"].sum().reset_index().sort_values("Amount", ascending=False).head(20)
    )
    top_products.to_csv(output_dir / "top_products_by_category.csv", index=False)

    print("Exported pipeline summary outputs to outputs/")


def main():
    raw_orders = load_raw_orders()
    cleaned = clean_orders(raw_orders)
    save_clean_file(cleaned)
    export_summary_files(cleaned)


if __name__ == "__main__":
    main()
