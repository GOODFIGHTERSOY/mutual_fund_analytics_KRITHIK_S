##SIP INFLOW
import pandas as pd
import sqlite3

conn=sqlite3.connect("sql\\bluestock_mf.db")
query="""SELECT
strftime('%Y', transaction_date) AS year,
SUM(amount_inr) AS sip_inflow
FROM fact_transactions
WHERE transaction_type = 'SIP'
GROUP BY year
ORDER BY year;"""
sd=pd.read_sql_query(query, conn)
print(sd)
sd.to_csv("reports/sip_inflow.csv", index=False)
print("CSV saved successfully!")