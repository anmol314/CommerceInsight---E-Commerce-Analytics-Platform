"""
Cohort Analysis Script
=====================
This script generates cohort analysis tables and visualizations for e-commerce data.
"""
import pandas as pd
import plotly.express as px
import os

def cohort_analysis(orders_path, output_path):
    orders = pd.read_csv(orders_path)
    orders['Order Date'] = pd.to_datetime(orders['Order Date'], errors='coerce')
    # Use 'CustomerName' as customer identifier
    orders['CohortMonth'] = orders.groupby('CustomerName')['Order Date'].transform('min').dt.to_period('M')
    orders['OrderMonth'] = orders['Order Date'].dt.to_period('M')
    cohort_data = orders.groupby(['CohortMonth', 'OrderMonth']).agg({'CustomerName':'nunique'}).reset_index()
    cohort_pivot = cohort_data.pivot(index='CohortMonth', columns='OrderMonth', values='CustomerName').fillna(0)
    cohort_pivot.to_csv(os.path.join(output_path, 'cohort_table.csv'))
    print('✓ Saved: cohort_table.csv')
    # Optional: Visualize retention
    # convert Period index/columns to string for compatibility with image engines
    display_pivot = cohort_pivot.copy()
    try:
        display_pivot.index = display_pivot.index.astype(str)
        display_pivot.columns = display_pivot.columns.astype(str)
    except Exception:
        pass
    fig = px.imshow(display_pivot, text_auto=True, aspect='auto', title='Cohort Retention Table')
    fig.write_image(os.path.join(output_path, 'cohort_retention.png'))
    print('✓ Saved: cohort_retention.png')

if __name__ == "__main__":
    BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DATA_PATH = os.path.join(BASE_PATH, 'data', 'merged_orders_cleaned.csv')
    OUTPUT_PATH = os.path.join(BASE_PATH, 'outputs')
    cohort_analysis(DATA_PATH, OUTPUT_PATH)
