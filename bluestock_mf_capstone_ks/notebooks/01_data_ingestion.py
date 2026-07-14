import pandas as pd
df1=pd.read_csv("data\\raw\\01_fund_master.csv")
print("df1",df1.shape)
print("df1",df1.head())
print("df1",df1.info())

df2=pd.read_csv("data\\raw\\02_nav_history.csv")
print("df2",df2.shape)
print("df2",df2.head())
print("df2",df2.info())

df3=pd.read_csv("data\\raw\\03_aum_by_fund_house.csv")
print("df3",df3.shape)
print("df3",df3.head())
print("df3",df3.info())

df4=pd.read_csv("data\\raw\\04_monthly_sip_inflows.csv")
print("df4",df4.shape)
print("df4",df4.head())
print("df4",df4.info())

df5=pd.read_csv("data\\raw\\05_category_inflows.csv")
print("df5",df5.shape)
print("df5",df5.head())
print("df5",df5.info())

df6=pd.read_csv("data\\raw\\06_industry_folio_count.csv")
print("df6",df6.shape)
print("df6",df6.head())
print("df6",df6.info())

df7=pd.read_csv("data\\raw\\07_scheme_performance.csv")
print("df7",df7.shape)
print("df7",df7.head())
print("df7",df7.info())

df8=pd.read_csv("data\\raw\\08_investor_transactions.csv")
print("df8",df8.shape)
print("df8",df8.head())
print("df8",df8.info())

df9=pd.read_csv("data\\raw\\09_portfolio_holdings.csv")
print("df9",df9.shape)
print("df9",df9.head())
print("df9",df9.info())

df10=pd.read_csv("data\\raw\\10_benchmark_indices.csv")
print("df10",df10.shape)
print("df10",df10.head())
print("df10",df10.info())
