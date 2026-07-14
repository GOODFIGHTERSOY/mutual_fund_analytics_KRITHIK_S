import pandas as pd
import sqlite3



conn = sqlite3.connect("sql\\bluestock_mf.db")
query="""
SELECT fund_house, aum_crore from fact_performance ORDER BY aum_crore DESC LIMIT 5;
"""

df = pd.read_sql_query(query, conn)

print(df)

df.to_csv("reports/top_5_funds_by_aum.csv", index=False)

print("CSV saved successfully!")

conn.close()



