# CommerceInsight Project Upgrade – Delivery Summary

## Completed Deliverables

### Stage 1: Interactive Dashboard Artifact ✅
**File:** `scripts/streamlit_dashboard.py`

The dashboard includes:
- **5 KPI cards**: Total Revenue (₹431.5K), Total Orders (500), Unique Customers (332), Average Order Value (₹863), North India Revenue Share (18.4%)
- **Punjab anomaly detection**: Identifies sales drops and alerts on regional issues
- **North India regional filter**: Interactive selection of states with live chart updates
- **Weekly sales area chart**: 24-week view showing regional trends by state
- **City-level drill-down**: Top 10 Punjab cities by revenue
- **Product category performance**: Horizontal bar charts with category breakdown

**Usage:**
```bash
pip install -r requirements.txt
python -m streamlit run scripts/streamlit_dashboard.py
```

### Stage 2: Portfolio Blueprint HTML ✅
**File:** `portfolio_blueprint.html`

A recruiter-facing narrative that explains:
- Problem statement: Regional sales anomaly detection for North India
- Architecture: Data → Pipeline → SQL Views → Dashboard
- Key messaging: Take-home evaluation readiness, North India focus, portfolio maturity
- Open in browser to demonstrate project story during interviews

### Stage 3: SQL + Python Pipeline ✅

#### Data Pipeline Script
**File:** `scripts/data_pipeline.py`
- Loads raw CSVs from `data/merged_orders.csv`
- Cleans date columns using `pd.to_datetime(format="%d-%m-%Y")`
- Engineers time features (Year, Month, Week, Quarter)
- Exports cleaned data to `data/merged_orders_cleaned.csv`
- Generates KPI, regional, and category summaries to `outputs/`

**Output files generated:**
- `kpi_summary.csv` – Revenue, orders, customers, AOV, North India share
- `weekly_sales_north_india.csv` – Weekly revenue by region
- `north_india_state_sales.csv` – State-level performance
- `punjab_weekly_trends.csv` – Punjab-specific anomaly tracking
- `top_products_by_category.csv` – Top 20 product categories

#### SQL Analytics Views
**File:** `sql/queries.sql`

New views added:
- `vw_north_india_sales` – State-level performance for North India states
- `vw_punjab_weekly_sales` – Week-over-week Punjab trends for anomaly detection
- `vw_top_product_categories` – Top 10 categories by revenue

---

## Project Statistics

**Dataset processed:**
- 500 orders across 332 customers
- 17 transaction fields (Order ID, Date, Customer, State, City, Amount, Profit, Quantity, Category, etc.)
- Geographic coverage: 28 states/regions, with 18.4% revenue from North India

**North India Focus:**
- 8 states targeted (Delhi, Haryana, Punjab, Uttar Pradesh, Uttarakhand, Himachal Pradesh, Jammu & Kashmir, Chandigarh)
- Punjab weekly anomaly tracking enabled
- Regional drill-down and city-level analysis

---

## How to Use for Recruitment

1. **Run the full pipeline:**
   ```bash
   python scripts/data_pipeline.py
   python run_analysis.py
   python scripts/rfm_analysis.py
   ```

2. **Launch the dashboard:**
   ```bash
   streamlit run scripts/streamlit_dashboard.py
   ```
   Live KPIs, anomaly alerts, and regional drill-downs demonstrate take-home evaluation capability.

3. **Review the portfolio story:**
   Open `portfolio_blueprint.html` in a browser.
   Use it as talking points during interviews to explain your analytics journey.

4. **Optional: Add Power BI screenshots**
   Place PNG files in `powerbi/dashboard_screenshots/` and reference them in notebooks.

---

## 2026 North India JDA Alignment

✅ **Real-time analytics**: Dashboard shows live KPIs and anomaly alerts  
✅ **Regional focus**: Punjab and North India states  
✅ **Take-home capability**: Runnable on local CSV uploads  
✅ **Business messaging**: KPI tracking, anomaly detection, drill-downs  
✅ **Technical stack**: Python, SQL, Streamlit, Plotly  
✅ **Portfolio narrative**: HTML blueprint explains business value to recruiters  

---

## File Structure

```
CommerceInsight/
├── data/
│   ├── merged_orders.csv                 (raw)
│   ├── merged_orders_cleaned.csv          (cleaned, pipeline output)
│   └── ...
├── outputs/
│   ├── kpi_summary.csv
│   ├── weekly_sales_north_india.csv
│   ├── north_india_state_sales.csv
│   ├── punjab_weekly_trends.csv
│   ├── top_products_by_category.csv
│   └── ...
├── scripts/
│   ├── streamlit_dashboard.py             (NEW: interactive dashboard)
│   ├── data_pipeline.py                   (NEW: ETL and export)
│   ├── analysis.py
│   ├── rfm_analysis.py
│   └── ...
├── sql/
│   ├── queries.sql                        (UPDATED: North India + Punjab views)
│   └── ...
├── notebooks/
│   ├── RFM_and_Sales_Analysis_Portfolio.ipynb
│   └── ...
├── requirements.txt                       (NEW: dependencies)
├── portfolio_blueprint.html                (NEW: recruiter narrative)
├── README.md                              (UPDATED: new instructions)
└── run_analysis.py                        (UPDATED: fixed paths)
```

---

## Next Steps (Optional Enhancements)

1. **Real-time data**: Connect to a live database instead of CSVs
2. **ML anomaly detection**: Use isolation forests or time-series models for Punjab trends
3. **Geocoding**: Map customer locations to actual coordinates
4. **Power BI export**: Add Plotly→Power BI integration for advanced dashboarding
5. **Retention modeling**: Extend RFM with churn prediction

---

**Ready for GitHub and recruitment!**
