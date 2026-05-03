"""
RFM Analysis Script
==================
This script performs RFM segmentation and saves the results for business use.
"""
import pandas as pd
import os

def rfm_analysis(orders_path, output_path):
    orders = pd.read_csv(orders_path)
    orders['Order Date'] = pd.to_datetime(orders['Order Date'], errors='coerce')
    # Use 'CustomerName' as customer identifier
    snapshot_date = orders['Order Date'].max() + pd.Timedelta(days=1)
    rfm = orders.groupby('CustomerName').agg({
        'Order Date': lambda x: (snapshot_date - x.max()).days,
        'Order ID': 'count',
        'Amount': 'sum'
    }).rename(columns={'Order Date': 'Recency', 'Order ID': 'Frequency', 'Amount': 'Monetary'})
    rfm['R_Score'] = pd.qcut(rfm['Recency'], 5, labels=[5,4,3,2,1])
    rfm['F_Score'] = pd.qcut(rfm['Frequency'].rank(method='first'), 5, labels=[1,2,3,4,5])
    rfm['M_Score'] = pd.qcut(rfm['Monetary'], 5, labels=[1,2,3,4,5])
    rfm['RFM_Segment'] = rfm['R_Score'].astype(str) + rfm['F_Score'].astype(str) + rfm['M_Score'].astype(str)
    rfm['RFM_Score'] = rfm[['R_Score','F_Score','M_Score']].astype(int).sum(axis=1)
    rfm['Segment'] = pd.qcut(rfm['RFM_Score'], 5, labels=['Lost','At Risk','Need Attention','Loyal','Champions'])
    rfm.to_csv(os.path.join(output_path, 'rfm_segments.csv'))
    print('✓ Saved: rfm_segments.csv')

if __name__ == "__main__":
    BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DATA_PATH = os.path.join(BASE_PATH, 'data', 'merged_orders_cleaned.csv')
    OUTPUT_PATH = os.path.join(BASE_PATH, 'outputs')
    rfm_analysis(DATA_PATH, OUTPUT_PATH)
