"""
ETL Pipeline

Description:
Extracts, cleans and transforms mutual fund datasets and
stores processed files for downstream analytics.

Author: Krithik
"""
import pandas as pd

df=pd.read_csv("data\\raw\\08_investor_transactions.csv")
df["transaction_type"]=df["transaction_type"].str.strip().str.upper()
#Invalid amount
invalid=df[df["annual_income_lakh"]<=0]
#Converting to datetime
df["transaction_date"]=pd.to_datetime(df["transaction_date"])

df["kyc_status"] = (df["kyc_status"].str.strip().str.upper())

df.to_csv("data\\processed\\clean_investor_transaction.csv", index=False)

##

import pandas as pd
df=pd.read_csv("data\\raw\\01_fund_master.csv")

df.sort_values(by=["amfi_code","launch_date"],inplace=True)

df["launch_date"]=pd.to_datetime(df["launch_date"])

df.drop_duplicates(inplace=True)
df.to_csv("data\\processed\\fund_master_clean.csv", index=False)

##
import pandas as pd
df=pd.read_csv("data\\raw\\02_nav_history.csv")

df["date"]=pd.to_datetime(df["date"])

df.sort_values(by=["amfi_code","date"],inplace=True)

df["nav"] = (df.groupby("amfi_code")["nav"].ffill())


df.drop_duplicates(inplace=True)


#Checking if nav>0
invalid=df[df["nav"]<=0]


df.to_csv("data\\processed\\clean_nav.csv", index=False)


##
import pandas as pd
df=pd.read_csv("data\\raw\\07_scheme_performance.csv")


# Checking expense ratio outliers
invalid = df[(df["expense_ratio_pct"] < 0.1) | (df["expense_ratio_pct"] > 2.5)]
print("Invalid expense ratios found:", len(invalid))

#Flagging invalid sharpe_ratio
print("Invalid Sharpe ratios found:", (df["sharpe_ratio"] < 0).sum())

df.to_csv("data\\processed\\clean_performance.csv", index=False)

##
import pandas as pd
df=pd.read_csv("data\\raw\\01_fund_master.csv")
print(df.head())
print(df.isnull().sum())
df.sort_values(by=["amfi_code","launch_date"],inplace=True)
print(df.head())
df["launch_date"]=pd.to_datetime(df["launch_date"])
print(df["launch_date"].head())

#Duplicate
print(df.duplicated().sum())

df.drop_duplicates(inplace=True)
df.to_csv("data\\processed\\fund_master_clean.csv", index=False)



import pandas as pd

# Read NAV data
nav = pd.read_csv("data\\processed\\clean_nav.csv")

# Convert date column
nav["date"] = pd.to_datetime(nav["date"])

# Sort data
nav = nav.sort_values(["amfi_code", "date"])

# Calculate daily return
nav["daily_return"] = nav.groupby("amfi_code")["nav"].pct_change()

# Annual Return
annual_return = (
    nav.groupby("amfi_code")["daily_return"]
       .apply(lambda x: ((1 + x.dropna()).prod())**(252/len(x.dropna())) - 1)
       .reset_index()
)

annual_return.columns = ["amfi_code", "annual_return"]

# Convert to percentage
annual_return["annual_return"] *= 100

# Save
annual_return.to_csv("data\\processed\\annual_return.csv", index=False)


