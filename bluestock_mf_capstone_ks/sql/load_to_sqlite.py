import pandas as pd
from sqlalchemy import create_engine
engine=create_engine('sqlite:///bluestock_mf.db')
fund_master = pd.read_csv("data\\processed\\fund_master_clean.csv")

nav_history = pd.read_csv("data\\processed\\clean_nav.csv")

transactions = pd.read_csv("data\\processed\\clean_investor_transaction.csv")

performance = pd.read_csv("data\\processed\\clean_performance.csv")

#Insert into tables
fund_master.to_sql("dim_fund",engine,if_exists="replace",index=False)

nav_history.to_sql("fact_nav",engine,if_exists="replace",index=False)

transactions.to_sql("fact_transactions",engine,if_exists="replace",index=False)

performance.to_sql("fact_performance",engine,if_exists="replace",index=False)