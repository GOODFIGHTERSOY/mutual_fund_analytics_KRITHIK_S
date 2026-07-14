# 📊 Mutual Fund Analytics Platform

A comprehensive Mutual Fund Analytics Platform built using **Python, SQLite, and Microsoft Power BI** to analyze mutual fund performance, investor behavior, and market trends. The project follows a complete data analytics workflow including ETL, financial metric computation, advanced analytics, and interactive dashboard visualization.

---

# Project Overview

This project aims to transform raw mutual fund datasets into meaningful business insights through data preprocessing, financial analysis, and interactive dashboards.

Major features include:

- ETL Pipeline
- Historical NAV Analysis
- Investor Analytics
- Financial Performance Metrics
- Risk Analysis (VaR & CVaR)
- Rolling Sharpe Ratio
- Portfolio Concentration Analysis (HHI)
- Mutual Fund Recommendation System
- Interactive Power BI Dashboard

---

# Technologies Used

- Python
- Pandas
- NumPy
- SQLite
- Power BI
- Matplotlib
- Scikit-learn

---

# Project Structure

```
bluestock_mf_capstone/
├── data/
│   ├── raw           ← original downloaded files
│   ├── processed     ← cleaned, merged CSVs
│   └── db            ← bluestock_mf.db (SQLite)
├── notebooks/
│   ├── 01_data_ingestion.ipynb
│   ├── 02_data_cleaning.ipynb
│   ├── 03_eda_analysis.ipynb
│   ├── 04_performance_analytics.ipynb
│   └── 05_advanced_analytics.ipynb
├── scripts/
│   ├── etl_pipeline.py
│   ├── live_nav_fetch.py
│   ├── compute_metrics.py
│   └── recommender.py
├── sql/
│   ├── bluestock_mf.db              # SQLite database
│   ├── mutual_fund.db               # Backup/alternate database
│   ├── create_database.py           # Creates SQLite database
│   ├── create_table.sql             # SQL table creation script
│   ├── load_to_sqlite.py            # Loads processed CSVs into SQLite
│   ├── queries.sql                  # Collection of SQL queries
│   ├── query_1.py                   # SQL Query Execution - 1
│   ├── query_2.py                   # SQL Query Execution - 2
│   ├── query_3.py                   # SQL Query Execution - 3
│   ├── query_4.py                   # SQL Query Execution - 4
│   ├── query_5.py                   # SQL Query Execution - 5
│   └── data_quality.txt             # Data quality validation report
├── dashboard/
│   └── bluestock_mf.pbix
├── reports/
│   ├── Final_Report.pdf
│   └── Presentation.pptx
└── README.md
```

---

# File Description

| File | Description |
|------|-------------|
| etl_pipeline.py | Cleans and transforms raw datasets into processed datasets |
| live_nav_fetch.py | Fetches latest NAV data using MFAPI |
| compute_metrics.py | Computes financial metrics such as CAGR, Sharpe Ratio, Alpha, Beta, VaR, CVaR and Rolling Sharpe Ratio |
| recommender.py | Rule-based mutual fund recommendation system |
| run_pipeline.py | Master script to execute the complete analytics workflow |
| Mutual_Fund_Dashboard.pbix | Interactive Power BI dashboard |
| Final_Report.pdf | Detailed project documentation |

---

# Setup Instructions

## Clone Repository

```bash
git clone <repository-url>
```

## Navigate to Project

```bash
cd bluestock_mf_capstone_ks
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Running the ETL Pipeline

Run the master pipeline:

```bash
cd scripts
python run_pipeline.py
```

This automatically executes:

- ETL Pipeline
- Live NAV Fetch
- Financial Metric Computation
- Recommendation Engine

---

# Opening the Dashboard

1. Open Microsoft Power BI Desktop.
2. Open:

```
dashboard/Mutual_Fund_Dashboard.pbix
```

3. Refresh the data if required.

The dashboard contains:

- Industry Overview
- Fund Performance
- Investor Analytics
- SIP & Market Trends

---

# Key Features

- Automated ETL Pipeline
- Historical NAV Analysis
- Investor Transaction Analysis
- Risk and Return Analytics
- Portfolio Diversification Analysis
- Interactive Power BI Dashboard
- Fund Recommendation System

---

# Author

**Krithik**



