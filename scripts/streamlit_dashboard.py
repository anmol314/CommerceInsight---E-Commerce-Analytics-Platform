import os
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

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


def load_data() -> pd.DataFrame:
    data_path = repo_root() / "data" / "merged_orders_cleaned.csv"
    if not data_path.exists():
        raise FileNotFoundError(
            f"Missing required dataset: {data_path}. Run the data pipeline first or add cleaned data."
        )

    df = pd.read_csv(data_path, parse_dates=["Order Date"], dayfirst=True)
    df["Order Date"] = pd.to_datetime(df["Order Date"], errors="coerce")
    df = df.dropna(subset=["Order Date"])
    df["Order Week"] = df["Order Date"].dt.to_period("W").apply(lambda p: p.start_time)
    df["North India"] = df["State"].isin(NORTH_INDIA_STATES)
    return df


def build_kpis(df: pd.DataFrame) -> dict:
    total_revenue = df["Amount"].sum()
    total_orders = df["Order ID"].nunique()
    total_customers = df["CustomerName"].nunique()
    aov = total_revenue / total_orders if total_orders else 0
    north_revenue = df.loc[df["North India"], "Amount"].sum()
    north_share = north_revenue / total_revenue if total_revenue else 0
    return {
        "Total Revenue": total_revenue,
        "Total Orders": total_orders,
        "Unique Customers": total_customers,
        "Average Order Value": aov,
        "North India Revenue Share": north_share,
    }


def detect_punjab_anomaly(df: pd.DataFrame) -> tuple[pd.DataFrame, float, bool]:
    punjab = df[df["State"] == "Punjab"]
    weekly = (
        punjab.groupby("Order Week")["Amount"].sum().reset_index().sort_values("Order Week")
    )
    recent = weekly.tail(8)
    prior = weekly.iloc[-16:-8]
    if len(prior) >= 4 and len(recent) >= 4:
        prior_avg = prior["Amount"].mean()
        recent_avg = recent["Amount"].mean()
        change = ((recent_avg - prior_avg) / prior_avg) if prior_avg else 0
        anomaly = change <= -0.20
    else:
        change = 0.0
        anomaly = False
    return weekly, change, anomaly


def format_currency(value: float) -> str:
    return f"₹{value:,.0f}"


def show_dashboard(df: pd.DataFrame):
    st.set_page_config(
        page_title="CommerceInsight North India Dashboard",
        page_icon="📈",
        layout="wide",
    )

    st.title("CommerceInsight 2026 | North India E-commerce Sales Dashboard")
    st.write(
        "This dashboard demonstrates a Junior Data Analyst-ready interactive analysis for North India, with KPI tracking, Punjab anomaly detection, and product/region drill-downs."
    )

    kpis = build_kpis(df)
    col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1])
    col1.metric("Total Revenue", format_currency(kpis["Total Revenue"]))
    col2.metric("Total Orders", f"{kpis['Total Orders']:,}")
    col3.metric("Unique Customers", f"{kpis['Unique Customers']:,}")
    col4.metric("Average Order Value", format_currency(kpis["Average Order Value"]))
    col5.metric("North India Revenue Share", f"{kpis['North India Revenue Share']:.1%}")

    north_only = st.checkbox("Focus on North India sales only", value=True)
    selected_states = st.multiselect(
        "Select states for regional comparison",
        options=NORTH_INDIA_STATES,
        default=NORTH_INDIA_STATES,
    )

    if north_only:
        chart_df = df[df["North India"] & df["State"].isin(selected_states)]
        note = "Applying North India state filter."
    else:
        chart_df = df[df["State"].isin(selected_states)]
        note = "Showing selected regional sales." if selected_states else "Showing all states."
    st.caption(note)

    weekly_chart = (
        chart_df.groupby(["Order Week", "State"])["Amount"].sum().reset_index()
    )
    fig = px.area(
        weekly_chart,
        x="Order Week",
        y="Amount",
        color="State",
        title="Weekly Sales Trend by State",
        labels={"Amount": "Sales (₹)", "Order Week": "Week"},
    )
    st.plotly_chart(fig, use_container_width=True)

    punjab_weekly, punjab_change, punjab_anomaly = detect_punjab_anomaly(df)
    if punjab_anomaly:
        st.warning(
            f"Punjab sales anomaly detected: weekly revenue has dropped by {punjab_change:.0%} compared to the prior period. Drill-down into the Punjab section for root cause signals."
        )
    else:
        st.info("No severe Punjab revenue anomaly detected in the latest period. Continue monitoring weekly trends.")

    st.subheader("Punjab Regional Drill-Down")
    punjab = df[df["State"] == "Punjab"]
    city_summary = (
        punjab.groupby("City")["Amount"].sum().reset_index().sort_values("Amount", ascending=False).head(10)
    )
    fig_city = px.bar(
        city_summary,
        x="Amount",
        y="City",
        orientation="h",
        title="Top 10 Cities by Punjab Revenue",
        labels={"Amount": "Revenue (₹)", "City": "City"},
    )
    st.plotly_chart(fig_city, use_container_width=True)

    top_categories = (
        df.groupby("Category")["Amount"].sum().reset_index().sort_values("Amount", ascending=False).head(10)
    )
    st.subheader("Top Product Categories")
    fig_cat = px.bar(
        top_categories,
        x="Amount",
        y="Category",
        orientation="h",
        title="Top 10 Categories by Revenue",
        labels={"Amount": "Revenue (₹)", "Category": "Category"},
        text="Amount",
    )
    fig_cat.update_traces(texttemplate="₹%{text:,.0f}", textposition="outside")
    st.plotly_chart(fig_cat, use_container_width=True)

    st.subheader("Top Products and Regional Insights")
    top_products = (
        df.groupby(["Category", "Sub-Category"])["Amount"].sum().reset_index().sort_values("Amount", ascending=False).head(12)
    )
    st.dataframe(
        top_products.assign(Amount=top_products["Amount"].map(lambda x: f"₹{x:,.0f}")),
        use_container_width=True,
    )

    st.markdown(
        "---"
        "\n**How to use this artifact:** Use the dashboard to show recruiters how you can turn transaction CSVs into business-ready KPIs, regional alerts, and North India performance insights."
    )
    st.caption(
        "Supports an interactive take-home evaluation with real-time KPI tracking and Punjab-focused anomaly exploration."
    )


if __name__ == "__main__":
    df = load_data()
    show_dashboard(df)
