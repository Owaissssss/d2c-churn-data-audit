# D2C Customer Churn Intelligence — Part 1: Data Audit & Business Explorations

[![Jupyter Notebook Preview](https://img.shields.io/badge/render-nbviewer-orange.svg)](https://nbviewer.org/github/Owaissssss/d2c-churn-data-audit/blob/master/eda_audit.ipynb)

This repository constitutes **Part 1** of the 4-part D2C Personal-Care Churn Intelligence Capstone Project. It contains full data sanity reports, operational leakage assessments, and code required to inspect initial user behavior before modeling workflows.

## Repository File Structure
* `requirements.txt`: Unified third-party dependency locks for reproducible testing environments.
* `eda_audit.ipynb`: Comprehensive notebook executing data transformations and outputting 6 core diagnostic charts.
* `data_quality_report.md`: Structured analytical report highlighting custom missing/anomaly counts and systemic leakage protection strategies.
* `business_memo.md`: Strategic executive alignment summary explaining domain churn hypotheses linked to behavioral anomalies.
* `outputs/`: Cached local directory housing high-resolution diagnostic distribution figures.

## Quick Execution Instructions
1. Initialize your isolated terminal framework and clear any legacy paths.
2. Install the locked dependencies from the root directory:
   ```bash
   pip install -r requirements.txt