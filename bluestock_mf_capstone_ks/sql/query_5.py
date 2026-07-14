import pandas as pd
import sqlite3
conn=sqlite3.connect("sql\\bluestock_mf.db")
query="""SELECT
d.scheme_name,
p.expense_ratio_pct
FROM fact_performance p
JOIN dim_fund d
ON p.amfi_code = d.amfi_code
WHERE p.expense_ratio_pct < 1
ORDER BY p.expense_ratio_pct;"""
df=pd.read_sql_query(query, conn)
df.to_csv("reports/expense_ratio_below_1.csv", index=False)
print("CSV saved successfully!")