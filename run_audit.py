import pandas as pd

# Load files
customers = pd.read_csv("customers.csv")
orders = pd.read_csv("orders.csv")
support = pd.read_csv("support_tickets.csv")
labels = pd.read_csv("churn_labels.csv")

print("\n==============================================")
print("     CAPSTONE PART 1 - INITIAL DATA METRICS    ")
print("==============================================")
print(f"Total rows in customers.csv : {len(customers)}")
print(f"Total rows in orders.csv    : {len(orders)}")
print(f"Total rows in support_tickets.csv: {len(support)}")
print(f"Total rows in churn_labels.csv  : {len(labels)}")

# Check for intentional design anomalies from Data Dictionary
dup_orders = orders['order_id'].str.endswith('_DUP').sum()
print(f"\n[Anomaly 1] Order IDs ending in '_DUP': {dup_orders}")

missing_loyalty = customers['loyalty_tier'].isna().sum()
missing_skin = customers['skin_type'].isna().sum()
print(f"[Anomaly 2] Missing loyalty_tier values: {missing_loyalty}")
print(f"[Anomaly 3] Missing skin_type values: {missing_skin}")

missing_ratings = orders['rating'].isna().sum()
print(f"[Anomaly 4] Orders with missing ratings: {missing_ratings}")

high_orders = (orders['gross_amount'] > 15000).sum()
print(f"[Anomaly 5] Outlier orders (> ₹15,000): {high_orders}")

future_orders = (pd.to_datetime(orders['order_date']) > '2025-09-30').sum()
print(f"[Leakage Risk] Orders placed after snapshot date (2025-09-30): {future_orders}")

churn_rate = labels['churn_next_60d'].mean() * 100
print(f"\nOverall Dataset Churn Rate: {churn_rate:.2f}%")
print("==============================================")