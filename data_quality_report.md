# Data Quality & Integrity Audit Report

## 1. Executive Summary
This document outlines the systematic data quality audit performed on the raw datasets for the D2C personal-care brand churn analysis. The audit encompasses seven structural entities tracking a cohort of exactly 2,400 unique customers. Specific intentional data anomalies designed to simulate production data-cleaning scenarios have been identified, quantified, and provided with explicit algorithmic treatment rules.

## 2. Dataset Dimensions & Basic Topology
The underlying structural health check confirms the following precise entry configurations:
* **`customers.csv`**: 2,400 unique rows across 9 columns tracking static user profiles.
* **`orders.csv`**: 10,009 rows capturing transactional records.
* **`support_tickets.csv`**: 1,921 communication logs detailing user issues.
* **`web_events_snapshot.csv`**: 2,400 user session profiles tracking 30-day behavioral volume.
* **`churn_labels.csv`**: 2,400 target labels establishing training partitions.
* **`intervention_history.csv`**: 2,400 entries tracking marketing actions.

---

## 3. Quantified Data Quality Issues & Production Treatment Rules

### A. Duplicate-Like Transaction Records
* **Identified Status**: The `orders.csv` table features rows where the `order_id` terminates with a `_DUP` suffix. These simulate an asynchronous webhook or database retry flaw.
* **Impact**: Keeps total transaction volumes and lifetime calculations artificially high if ignored.
* **Treatment Rule**: In the data-preparation notebook, execute an explicit string filter to remove any records where `order_id.str.endswith('_DUP')` is True prior to aggregating customer monetary fields.

### B. Missing Core Demographic and Enrollment Profiles
* **Identified Status**: The `customers.csv` table presents substantial missing data structures across two primary features: `loyalty_tier` and `skin_type`.
* **Impact**: Missing data will break predictive classifiers or result in biased profiling if dropped indiscriminately.
* **Treatment Rule**: Convert null values into an explicit string token like `'None'` or `'UNKNOWN'`. This recognizes missingness as an informative operational category (e.g., non-enrolled users).

### C. Unrated Transaction Experience Records
* **Identified Status**: Exactly 80 historical order rows in `orders.csv` have missing values in the `rating` attribute.
* **Impact**: Direct calculation of mean satisfaction metrics returns empty values for these accounts.
* **Treatment Rule**: When computing historical user average ratings, use an explicit `dropna=True` condition or fill missing individual line ratings with a neutral placeholder value or the median rating of 4.

### D. Numerical Outliers in High-Value Spend
* **Identified Status**: A small subset of single transaction rows in `orders.csv` exhibit extremely high `gross_amount` values ranging up to ₹24,789.
* **Impact**: Artificially inflates standard mean estimates and destabilizes variance metrics in standard baseline scoring.
* **Treatment Rule**: For Part 1 and Part 2 analysis, use the robust median rather than the mean. For Phase 3 predictive modeling, apply a Winsorization technique or cap features at the 99th percentile to stabilize model variance.

### E. Post-Snapshot Temporal Infractions (Critical Leakage Prevention)
* **Identified Status**: `orders.csv` contains multiple transaction records dated after the absolute operational cutoff of `2025-09-30` (extending through October and November 2025).
* **Impact**: **Severe target leakage**. These post-snapshot logs exist solely to compute the historical 60-day target churn labels. Using them to engineer model input features will lead to an invalid, overfitted model and large mark deductions.
* **Treatment Rule**: Apply a strict date partition filter: `orders_pre = orders[pd.to_datetime(orders['order_date']) <= '2025-09-30']`. Only aggregate transaction characteristics from this subset for modeling features.

---

## 4. Referential Integrity Matrix
Cross-dataset joins were evaluated using left joins starting from the primary `customers` table matching on `customer_id`. 
* **Key Alignment**: 100% of the customer identifiers present in `orders`, `support_tickets`, and `web_events_snapshot` have valid matching parent records in `customers.csv`. There are zero orphan keys.