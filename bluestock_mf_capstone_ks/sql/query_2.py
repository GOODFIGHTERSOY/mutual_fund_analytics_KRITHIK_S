import pandas as pd
import sqlite3



conn = sqlite3.connect("sql\\bluestock_mf.db")
query="""
SELECT
strftime('%Y-%m', date) AS month,
ROUND(AVG(nav), 2) AS avg_nav
FROM fact_nav
GROUP BY month
ORDER BY month;
"""

df = pd.read_sql_query(query, conn)

print(df)

df.to_csv("reports/monthly_avg_nav.csv", index=False)

print("CSV saved successfully!")

conn.close()
