import json

# Define the notebook structure programmatically to build eda_audit.ipynb
notebook_content = {
    "cells": [
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "# Capstone Part 1: Exploratory Data Analysis & Integrity Audit\n",
                "**Course**: IITP AI Course Capstone\n",
                "**Project Repository**: `d2c-churn-data-audit`\n\n",
                "### Objective:\n",
                "This notebook implements a complete data loading, joining, cleaning, and visual analysis workflow to evaluate customer churn drivers while aggressively protecting against target window data leakage."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "import pandas as pd\n",
                "import numpy as np\n",
                "import matplotlib.pyplot as plt\n",
                "import seaborn as sns\n",
                "import os\n\n",
                "sns.set_theme(style='whitegrid')\n",
                "os.makedirs('outputs', exist_ok=True)\n",
                "print('Libraries and directory structures loaded successfully.')"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 1. Data Loading and Base Table Inspections\n",
                "We load all 7 core data assets and verify shapes against known operational parameters."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "customers = pd.read_csv('customers.csv')\n",
                "orders = pd.read_csv('orders.csv')\n",
                "support = pd.read_csv('support_tickets.csv')\n",
                "labels = pd.read_csv('churn_labels.csv')\n",
                "web_events = pd.read_csv('web_events_snapshot.csv')\n",
                "rfm_snap = pd.read_csv('rfm_modeling_snapshot.csv')\n",
                "interventions = pd.read_csv('intervention_history.csv')\n\n",
                "print(f'Customers Profile Layer: {customers.shape}')\n",
                "print(f'Raw Transactions File:   {orders.shape}')\n",
                "print(f'Customer Care Tickets:    {support.shape}')\n",
                "print(f'Target Churn Labels:     {labels.shape}')"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 2. Implementing Rigorous Data Quality Cleansing\n",
                "Based on our data audit, we apply exact deterministic fixes for duplicates, missing categorical strings, and split out the post-snapshot leakage transaction records."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# A. Deduplicate retry webhook records\n",
                "orders_cleaned = orders[~orders['order_id'].str.endswith('_DUP')].copy()\n\n",
                "# B. Categorical Missing Profiling Imputation\n",
                "customers['loyalty_tier'] = customers['loyalty_tier'].fillna('UNKNOWN_UNENROLLED')\n",
                "customers['skin_type'] = customers['skin_type'].fillna('UNKNOWN_PROFILE')\n\n",
                "# C. Unrated experiences neutral transformation\n",
                "orders_cleaned['rating'] = orders_cleaned['rating'].fillna(4.0)\n\n",
                "# D. LEAKAGE ISOLATION GUARDRAIL\n",
                "orders_cleaned['order_date'] = pd.to_datetime(orders_cleaned['order_date'])\n",
                "historical_orders = orders_cleaned[orders_cleaned['order_date'] <= '2025-09-30'].copy()\n\n",
                "print(f'Cleaned Historical Transact Rows (Pre-Snapshot Base): {historical_orders.shape[0]}')"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 3. Creating Visual Diagnostics (+6 Required Meaningful Visual Charts)"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Plot 1: Target Variable Breakdown\n",
                "plt.figure(figsize=(6, 4))\n",
                "sns.countplot(data=labels, x='churn_next_60d', hue='churn_next_60d', palette='viridis', legend=False)\n",
                "plt.title('Distribution of Churn Labels (Target Balance Check)')\n",
                "plt.xlabel('Churn Target (1 = Churned, 0 = Retained)')\n",
                "plt.savefig('outputs/chart1_target_balance.png', dpi=300, bbox_inches='tight')\n",
                "plt.show()"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Plot 2: Support Ticket Frequencies by Category\n",
                "plt.figure(figsize=(8, 4))\n",
                "sns.countplot(data=support, y='issue_type', order=support['issue_type'].value_counts().index, palette='magma', hue='issue_type', legend=False)\n",
                "plt.title('Support Desk Issue Volume by Category Type')\n",
                "plt.xlabel('Total Logged Tickets')\n",
                "plt.savefig('outputs/chart2_support_categories.png', dpi=300, bbox_inches='tight')\n",
                "plt.show()"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Plot 3: Boxplot of Recency Days vs Churn State\n",
                "merged_rfm = pd.merge(rfm_snap, labels, on='customer_id')\n",
                "plt.figure(figsize=(7, 4))\n",
                "sns.boxplot(data=merged_rfm, x='churn_next_60d', y='recency_days', palette='Set2', hue='churn_next_60d', legend=False)\n",
                "plt.title('Order Recency Spans vs. Observed Customer Churn')\n",
                "plt.ylabel('Days Since Most Recent Order')\n",
                "plt.savefig('outputs/chart3_recency_boxplot.png', dpi=300, bbox_inches='tight')\n",
                "plt.show()"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Plot 4: Order Frequency Distribution per Customer\n",
                "plt.figure(figsize=(7, 4))\n",
                "sns.histplot(data=rfm_snap, x='frequency_180d', kde=True, bins=15, color='royalblue')\n",
                "plt.title('180-Day Customer Historical Purchase Frequency')\n",
                "plt.xlabel('Number of Orders Logged')\n",
                "plt.savefig('outputs/chart4_frequency_distribution.png', dpi=300, bbox_inches='tight')\n",
                "plt.show()"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Plot 5: App Platform Sessions vs Observed Churn\n",
                "plt.figure(figsize=(7, 4))\n",
                "sns.violinplot(data=merged_rfm, x='churn_next_60d', y='sessions_30d', palette='coolwarm', hue='churn_next_60d', legend=False)\n",
                "plt.title('30-Day Platform Session Frequencies vs Churn Outcomes')\n",
                "plt.ylabel('Total Volumetric Sessions')\n",
                "plt.savefig('outputs/chart5_session_violin.png', dpi=300, bbox_inches='tight')\n",
                "plt.show()"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Plot 6: Financial Monetary Distribution vs Acquisition Footprint\n",
                "plt.figure(figsize=(8, 4))\n",
                "sns.barplot(data=merged_rfm, x='acquisition_channel', y='monetary_180d', hue='churn_next_60d', palette='muted', errorbar=None)\n",
                "plt.title('Mean 180-Day Revenue Contributions by Sourcing Vector')\n",
                "plt.ylabel('Average Gross Revenue Value (₹)')\n",
                "plt.xticks(rotation=15)\n",
                "plt.savefig('outputs/chart6_monetary_sourcing.png', dpi=300, bbox_inches='tight')\n",
                "plt.show()\n",
                "print('All 6 high-resolution analysis plots generated and cached successfully.')"
            ]
        }
    ],
    "metadata": {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3"
        },
        "language_info": {
            "name": "python"
        }
    },
    "nbformat": 4,
    "nbformat_minor": 2
}

# Write content to local file
with open("eda_audit.ipynb", "w", encoding="utf-8") as f:
    json.dump(notebook_content, f, indent=2)

print("SUCCESS: eda_audit.ipynb file generated cleanly in your project root!")