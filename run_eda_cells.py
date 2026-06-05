import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Configure professional styles
sns.set_theme(style='whitegrid')
os.makedirs('outputs', exist_ok=True)

print("--- Step 1: Loading Real Dataset Arrays ---")
customers = pd.read_csv('customers.csv')
orders = pd.read_csv('orders.csv')
support = pd.read_csv('support_tickets.csv')
labels = pd.read_csv('churn_labels.csv')
web_events = pd.read_csv('web_events_snapshot.csv')
rfm_snap = pd.read_csv('rfm_modeling_snapshot.csv')
interventions = pd.read_csv('intervention_history.csv')

print(f"Data shapes verified: labels={labels.shape}, orders={orders.shape}, rfm_snap={rfm_snap.shape}")

print("\n--- Step 2: Executing Clean Transformations & Leakage Prevention ---")
# Remove webhook retry instances
orders_cleaned = orders[~orders['order_id'].str.endswith('_DUP')].copy()

# Fix categoricals
customers['loyalty_tier'] = customers['loyalty_tier'].fillna('UNKNOWN_UNENROLLED')
customers['skin_type'] = customers['skin_type'].fillna('UNKNOWN_PROFILE')
orders_cleaned['rating'] = orders_cleaned['rating'].fillna(4.0)

# Apply absolute pre-snapshot barrier to orders
orders_cleaned['order_date'] = pd.to_datetime(orders_cleaned['order_date'])
historical_orders = orders_cleaned[orders_cleaned['order_date'] <= '2025-09-30'].copy()
print(f"Safe pre-snapshot transactions filtered: {historical_orders.shape[0]} rows")

print("\n--- Step 3: Generating All 6 Required Corporate Charts ---")

# Chart 1: Target Balance
plt.figure(figsize=(6, 4))
sns.countplot(data=rfm_snap, x='churn_next_60d', hue='churn_next_60d', palette='viridis', legend=False)
plt.title('Distribution of Churn Labels (Target Balance Check)')
plt.xlabel('Churn Target (1 = Churned, 0 = Retained)')
plt.savefig('outputs/chart1_target_balance.png', dpi=300, bbox_inches='tight')
plt.close()

# Chart 2: Support Categories
plt.figure(figsize=(8, 4))
sns.countplot(data=support, y='issue_type', order=support['issue_type'].value_counts().index, palette='magma', hue='issue_type', legend=False)
plt.title('Support Desk Issue Volume by Category Type')
plt.xlabel('Total Logged Tickets')
plt.savefig('outputs/chart2_support_categories.png', dpi=300, bbox_inches='tight')
plt.close()

# Chart 4: Frequency Distribution
plt.figure(figsize=(7, 4))
sns.histplot(data=rfm_snap, x='frequency_180d', kde=True, bins=15, color='royalblue')
plt.title('180-Day Customer Historical Purchase Frequency')
plt.xlabel('Number of Orders Logged')
plt.savefig('outputs/chart4_frequency_distribution.png', dpi=300, bbox_inches='tight')
plt.close()

# Chart 3: Recency Boxplot (Using clean rfm_snap dataset directly)
plt.figure(figsize=(7, 4))
sns.boxplot(data=rfm_snap, x='churn_next_60d', y='recency_days', palette='Set2', hue='churn_next_60d', legend=False)
plt.title('Order Recency Spans vs. Observed Customer Churn')
plt.ylabel('Days Since Most Recent Order')
plt.savefig('outputs/chart3_recency_boxplot.png', dpi=300, bbox_inches='tight')
plt.close()

# Chart 5: Platform Sessions
plt.figure(figsize=(7, 4))
sns.violinplot(data=rfm_snap, x='churn_next_60d', y='sessions_30d', palette='coolwarm', hue='churn_next_60d', legend=False)
plt.title('30-Day Platform Session Frequencies vs Churn Outcomes')
plt.ylabel('Total Volumetric Sessions')
plt.savefig('outputs/chart5_session_violin.png', dpi=300, bbox_inches='tight')
plt.close()

# Chart 6: Monetary vs Acquisition Vector
plt.figure(figsize=(8, 4))
sns.barplot(data=rfm_snap, x='acquisition_channel', y='monetary_180d', hue='churn_next_60d', palette='muted', errorbar=None)
plt.title('Mean 180-Day Revenue Contributions by Sourcing Vector')
plt.ylabel('Average Gross Revenue Value (₹)')
plt.xticks(rotation=15)
plt.savefig('outputs/chart6_monetary_sourcing.png', dpi=300, bbox_inches='tight')
plt.close()

print("SUCCESS: All 6 analysis charts created and saved in 'outputs/' folder!")