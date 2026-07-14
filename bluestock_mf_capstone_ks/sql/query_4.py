import pandas as pd
import sqlite3
conn=sqlite3.connect("sql\\bluestock_mf.db")
query="""SELECT
state,
COUNT(*) AS total_transactions,
SUM(amount_inr) AS total_amount
FROM fact_transactions
GROUP BY state
ORDER BY total_amount DESC;"""
df=pd.read_sql_query(query, conn)
print(df)
df.to_csv("reports/transactions_by_state.csv", index=False)
print("CSV saved successfully!")