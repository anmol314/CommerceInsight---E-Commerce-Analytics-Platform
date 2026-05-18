"""
Combined E-Commerce Analytics Project
=======================================
This script runs comprehensive analysis on both datasets and saves results.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from datetime import datetime

# Set paths relative to the repository root
BASE_PATH = os.path.abspath(os.path.dirname(__file__))
DATA_PATH = os.path.join(BASE_PATH, "data")
OUTPUT_PATH = os.path.join(BASE_PATH, "outputs")

# Create outputs directory if not exists
os.makedirs(OUTPUT_PATH, exist_ok=True)

# Set visualization style
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("husl")

print("=" * 60)
print("COMBINED E-COMMERCE ANALYTICS PROJECT")
print("=" * 60)
print(f"\nStarted at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

# ============================================================
# SECTION 1: Load Data from Project 1 (Marketing Analytics)
# ============================================================
print("=" * 60)
print("LOADING PROJECT 1: MARKETING ANALYTICS DATA")
print("=" * 60)

try:
    customers = pd.read_csv(os.path.join(DATA_PATH, "CUSTOMERS.csv"))
    print(f"✓ CUSTOMERS.csv loaded: {len(customers):,} records")
except Exception as e:
    print(f"✗ Error loading CUSTOMERS.csv: {e}")
    customers = None

try:
    products = pd.read_csv(os.path.join(DATA_PATH, "PRODUCTS.csv"))
    print(f"✓ PRODUCTS.csv loaded: {len(products):,} records")
except Exception as e:
    print(f"✗ Error loading PRODUCTS.csv: {e}")
    products = None

try:
    sellers = pd.read_csv(os.path.join(DATA_PATH, "SELLERS.csv"))
    print(f"✓ SELLERS.csv loaded: {len(sellers):,} records")
except Exception as e:
    print(f"✗ Error loading SELLERS.csv: {e}")
    sellers = None

try:
    order_payments = pd.read_csv(os.path.join(DATA_PATH, "ORDER_PAYMENTS.csv"))
    print(f"✓ ORDER_PAYMENTS.csv loaded: {len(order_payments):,} records")
except Exception as e:
    print(f"✗ Error loading ORDER_PAYMENTS.csv: {e}")
    order_payments = None

try:
    order_reviews = pd.read_csv(os.path.join(DATA_PATH, "ORDER_REVIEW_RATINGS.csv"))
    print(f"✓ ORDER_REVIEW_RATINGS.csv loaded: {len(order_reviews):,} records")
except Exception as e:
    print(f"✗ Error loading ORDER_REVIEW_RATINGS.csv: {e}")
    order_reviews = None

try:
    geo_location = pd.read_csv(os.path.join(DATA_PATH, "GEO_LOCATION.csv"))
    print(f"✓ GEO_LOCATION.csv loaded: {len(geo_location):,} records")
except Exception as e:
    print(f"✗ Error loading GEO_LOCATION.csv: {e}")
    geo_location = None

# ============================================================
# SECTION 2: Load Data from Project 2 (Sales Analysis)
# ============================================================
print("\n" + "=" * 60)
print("LOADING PROJECT 2: SALES ANALYSIS DATA")
print("=" * 60)

try:
    list_of_orders = pd.read_csv(os.path.join(DATA_PATH, "List of Orders.csv"))
    print(f"✓ List of Orders.csv loaded: {len(list_of_orders):,} records")
except Exception as e:
    print(f"✗ Error loading List of Orders.csv: {e}")
    list_of_orders = None

try:
    order_details = pd.read_csv(os.path.join(DATA_PATH, "Order Details.csv"))
    print(f"✓ Order Details.csv loaded: {len(order_details):,} records")
except Exception as e:
    print(f"✗ Error loading Order Details.csv: {e}")
    order_details = None

try:
    merged_orders = pd.read_csv(os.path.join(DATA_PATH, "merged_orders_cleaned.csv"))
    print(f"✓ merged_orders_cleaned.csv loaded: {len(merged_orders):,} records")
except Exception as e:
    print(f"✗ Error loading merged_orders_cleaned.csv: {e}")
    merged_orders = None

try:
    monthly_sales = pd.read_csv(os.path.join(DATA_PATH, "monthly_sales.csv"))
    print(f"✓ monthly_sales.csv loaded: {len(monthly_sales):,} records")
except Exception as e:
    print(f"✗ Error loading monthly_sales.csv: {e}")
    monthly_sales = None

# ============================================================
# SECTION 3: Marketing Analytics (Project 1)
# ============================================================
print("\n" + "=" * 60)
print("ANALYSIS 1: MARKETING ANALYTICS")
print("=" * 60)

marketing_results = {}

# Customer Analysis
if customers is not None:
    print("\n--- Customer Analysis ---")
    marketing_results['total_customers'] = len(customers)
    marketing_results['unique_states'] = customers['customer_state'].nunique()
    marketing_results['top_state'] = customers['customer_state'].value_counts().idxmax()
    print(f"Total Customers: {marketing_results['total_customers']:,}")
    print(f"Unique States: {marketing_results['unique_states']}")
    print(f"Top State: {marketing_results['top_state']}")
    
    # Save customer summary
    customer_summary = customers['customer_state'].value_counts().head(10)
    customer_summary.to_csv(os.path.join(OUTPUT_PATH, "top_states_by_customers.csv"))
    print("✓ Saved: top_states_by_customers.csv")

# Product Analysis
if products is not None:
    print("\n--- Product Analysis ---")
    marketing_results['total_products'] = len(products)
    marketing_results['unique_categories'] = products['product_category_name'].nunique()
    print(f"Total Products: {marketing_results['total_products']:,}")
    print(f"Unique Categories: {marketing_results['unique_categories']}")
    
    # Save product summary
    product_summary = products['product_category_name'].value_counts().head(10)
    product_summary.to_csv(os.path.join(OUTPUT_PATH, "top_product_categories.csv"))
    print("✓ Saved: top_product_categories.csv")

# Payment Analysis
if order_payments is not None:
    print("\n--- Payment Analysis ---")
    marketing_results['total_payments'] = len(order_payments)
    marketing_results['avg_payment_value'] = order_payments['payment_value'].mean()
    marketing_results['top_payment_type'] = order_payments['payment_type'].value_counts().idxmax()
    print(f"Total Payments: {marketing_results['total_payments']:,}")
    print(f"Average Payment Value: ${marketing_results['avg_payment_value']:.2f}")
    print(f"Top Payment Type: {marketing_results['top_payment_type']}")
    
    # Save payment summary
    payment_summary = order_payments['payment_type'].value_counts()
    payment_summary.to_csv(os.path.join(OUTPUT_PATH, "payment_type_distribution.csv"))
    print("✓ Saved: payment_type_distribution.csv")

# Review Analysis
if order_reviews is not None:
    print("\n--- Review Analysis ---")
    marketing_results['total_reviews'] = len(order_reviews)
    marketing_results['avg_rating'] = order_reviews['review_score'].mean()
    print(f"Total Reviews: {marketing_results['total_reviews']:,}")
    print(f"Average Review Score: {marketing_results['avg_rating']:.2f}")
    
    # Save review summary
    review_summary = order_reviews['review_score'].value_counts().sort_index()
    review_summary.to_csv(os.path.join(OUTPUT_PATH, "review_score_distribution.csv"))
    print("✓ Saved: review_score_distribution.csv")

# Seller Analysis
if sellers is not None:
    print("\n--- Seller Analysis ---")
    marketing_results['total_sellers'] = len(sellers)
    marketing_results['seller_unique_states'] = sellers['seller_state'].nunique()
    print(f"Total Sellers: {marketing_results['total_sellers']:,}")
    print(f"Seller States: {marketing_results['seller_unique_states']}")
    
    # Save seller summary
    seller_summary = sellers['seller_state'].value_counts().head(10)
    seller_summary.to_csv(os.path.join(OUTPUT_PATH, "top_states_by_sellers.csv"))
    print("✓ Saved: top_states_by_sellers.csv")

# ============================================================
# SECTION 4: Sales Analytics (Project 2)
# ============================================================
print("\n" + "=" * 60)
print("ANALYSIS 2: SALES ANALYTICS")
print("=" * 60)

sales_results = {}

# Monthly Sales Analysis
if monthly_sales is not None:
    print("\n--- Monthly Sales Trends ---")
    sales_results['months_of_data'] = len(monthly_sales)
    sales_results['total_sales_value'] = monthly_sales['Total_Sales'].sum() if 'Total_Sales' in monthly_sales.columns else 0
    print(f"Months of Data: {sales_results['months_of_data']}")
    print(f"Total Sales Value: ${sales_results['total_sales_value']:,.2f}")
    
    # Save monthly sales
    monthly_sales.to_csv(os.path.join(OUTPUT_PATH, "monthly_sales_analysis.csv"), index=False)
    print("✓ Saved: monthly_sales_analysis.csv")

# Order Details Analysis
if order_details is not None:
    print("\n--- Order Details Analysis ---")
    sales_results['total_orders'] = len(order_details)
    if 'Amount' in order_details.columns:
        sales_results['total_revenue'] = order_details['Amount'].sum()
        sales_results['avg_order_value'] = order_details['Amount'].mean()
        print(f"Total Orders: {sales_results['total_orders']:,}")
        print(f"Total Revenue: ${sales_results['total_revenue']:,.2f}")
        print(f"Average Order Value: ${sales_results['avg_order_value']:.2f}")
    
    # Category analysis
    if 'Category' in order_details.columns:
        category_sales = order_details.groupby('Category')['Amount'].sum().sort_values(ascending=False)
        category_sales.to_csv(os.path.join(OUTPUT_PATH, "category_sales_combined.csv"))
        print("✓ Saved: category_sales_combined.csv")
    
    # Sub-category analysis
    if 'Sub-Category' in order_details.columns:
        subcategory_sales = order_details.groupby('Sub-Category')['Amount'].sum().sort_values(ascending=False)
        subcategory_sales.head(10).to_csv(os.path.join(OUTPUT_PATH, "subcategory_sales_top10.csv"))
        print("✓ Saved: subcategory_sales_top10.csv")

# List of Orders Analysis
if list_of_orders is not None:
    print("\n--- Order List Analysis ---")
    sales_results['total_list_orders'] = len(list_of_orders)
    print(f"Total Orders in List: {sales_results['total_list_orders']:,}")
    
    # State analysis - use 'State' column
    if 'State' in list_of_orders.columns:
        state_sales = list_of_orders.groupby('State').size().sort_values(ascending=False)
        state_sales.to_csv(os.path.join(OUTPUT_PATH, "state_orders_combined.csv"))
        print("✓ Saved: state_orders_combined.csv")

# Merged Orders Analysis
if merged_orders is not None:
    print("\n--- Merged Orders Analysis ---")
    sales_results['merged_orders_count'] = len(merged_orders)
    print(f"Merged Orders: {sales_results['merged_orders_count']:,}")
    
    # Save merged orders summary
    merged_orders.to_csv(os.path.join(OUTPUT_PATH, "merged_orders_summary.csv"), index=False)
    print("✓ Saved: merged_orders_summary.csv")

# ============================================================
# SECTION 5: Visualizations
# ============================================================
print("\n" + "=" * 60)
print("GENERATING VISUALIZATIONS")
print("=" * 60)

# Visualization 1: Payment Type Distribution
if order_payments is not None:
    plt.figure(figsize=(10, 6))
    payment_counts = order_payments['payment_type'].value_counts()
    payment_counts.plot(kind='bar', color=sns.color_palette("husl", len(payment_counts)))
    plt.title('Payment Type Distribution', fontsize=14, fontweight='bold')
    plt.xlabel('Payment Type')
    plt.ylabel('Count')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_PATH, "viz_payment_types.png"), dpi=150)
    plt.close()
    print("✓ Saved: viz_payment_types.png")

# Visualization 2: Review Score Distribution
if order_reviews is not None:
    plt.figure(figsize=(10, 6))
    review_counts = order_reviews['review_score'].value_counts().sort_index()
    review_counts.plot(kind='bar', color=sns.color_palette("RdYlGn", len(review_counts)))
    plt.title('Review Score Distribution', fontsize=14, fontweight='bold')
    plt.xlabel('Review Score')
    plt.ylabel('Count')
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_PATH, "viz_review_scores.png"), dpi=150)
    plt.close()
    print("✓ Saved: viz_review_scores.png")

# Visualization 3: Top Product Categories
if products is not None:
    plt.figure(figsize=(12, 6))
    top_categories = products['product_category_name'].value_counts().head(15)
    top_categories.plot(kind='barh', color=sns.color_palette("viridis", len(top_categories)))
    plt.title('Top 15 Product Categories', fontsize=14, fontweight='bold')
    plt.xlabel('Number of Products')
    plt.ylabel('Category')
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_PATH, "viz_top_categories.png"), dpi=150)
    plt.close()
    print("✓ Saved: viz_top_categories.png")

# Visualization 4: Monthly Sales Trend
if monthly_sales is not None and 'Month_Name' in monthly_sales.columns:
    plt.figure(figsize=(12, 6))
    plt.plot(monthly_sales['Month_Name'], monthly_sales['Total_Sales'], marker='o', linewidth=2, color='#2E86AB')
    plt.title('Monthly Sales Trend', fontsize=14, fontweight='bold')
    plt.xlabel('Month')
    plt.ylabel('Sales')
    plt.xticks(rotation=45)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_PATH, "viz_monthly_sales.png"), dpi=150)
    plt.close()
    print("✓ Saved: viz_monthly_sales.png")

# Visualization 5: Customer State Distribution
if customers is not None:
    plt.figure(figsize=(12, 6))
    top_states = customers['customer_state'].value_counts().head(15)
    top_states.plot(kind='bar', color=sns.color_palette("Spectral", len(top_states)))
    plt.title('Top 15 States by Customer Count', fontsize=14, fontweight='bold')
    plt.xlabel('State')
    plt.ylabel('Number of Customers')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_PATH, "viz_customer_states.png"), dpi=150)
    plt.close()
    print("✓ Saved: viz_customer_states.png")

# ============================================================
# SECTION 6: Summary Report
# ============================================================
print("\n" + "=" * 60)
print("GENERATING SUMMARY REPORT")
print("=" * 60)

# Combine all results
summary_data = {
    'Metric': [],
    'Value': [],
    'Source': []
}

# Add marketing results
for key, value in marketing_results.items():
    summary_data['Metric'].append(key.replace('_', ' ').title())
    summary_data['Value'].append(str(value))
    summary_data['Source'].append('Project 1: Marketing Analytics')

# Add sales results
for key, value in sales_results.items():
    summary_data['Metric'].append(key.replace('_', ' ').title())
    summary_data['Value'].append(str(value))
    summary_data['Source'].append('Project 2: Sales Analysis')

summary_df = pd.DataFrame(summary_data)
summary_df.to_csv(os.path.join(OUTPUT_PATH, "combined_summary.csv"), index=False)
print("✓ Saved: combined_summary.csv")

# ============================================================
# FINAL SUMMARY
# ============================================================
print("\n" + "=" * 60)
print("ANALYSIS COMPLETE!")
print("=" * 60)

print(f"\n📊 SUMMARY OF RESULTS:")
print("-" * 40)

if customers is not None:
    print(f"• Customers: {len(customers):,}")
if products is not None:
    print(f"• Products: {len(products):,}")
if sellers is not None:
    print(f"• Sellers: {len(sellers):,}")
if order_payments is not None:
    print(f"• Payments: {len(order_payments):,}")
if order_reviews is not None:
    print(f"• Reviews: {len(order_reviews):,}")
if order_details is not None:
    print(f"• Order Details: {len(order_details):,}")
if monthly_sales is not None:
    print(f"• Monthly Sales Records: {len(monthly_sales):,}")

print(f"\n📁 Output files saved to: {OUTPUT_PATH}")
print(f"\n✅ Analysis completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")