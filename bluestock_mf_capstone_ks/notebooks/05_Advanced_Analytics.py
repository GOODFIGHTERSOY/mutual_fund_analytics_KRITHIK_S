import pandas as pd
df=pd.read_csv("data\\processed\\clean_nav.csv")

# Sort by fund and date
df = df.sort_values(['amfi_code', 'date'])

# Daily return
df['daily_return'] = df.groupby('amfi_code')['nav'].pct_change()

# Remove NaN values
df = df.dropna(subset=['daily_return'])
#historical VAR 95%
var95 = (
    df.groupby('amfi_code')['daily_return']
      .quantile(0.05)
      .reset_index()
)

var95.columns = ['amfi_code', 'VaR_95']

#Calculating CVaR
cvar = []

for fund in df['amfi_code'].unique():

    temp = df[df['amfi_code'] == fund]

    var = temp['daily_return'].quantile(0.05)

    cvar_value = temp[temp['daily_return'] <= var]['daily_return'].mean()

    cvar.append([fund, cvar_value])

cvar = pd.DataFrame(cvar, columns=['amfi_code', 'CVaR_95'])

risk_metrics = pd.merge(var95, cvar, on='amfi_code')
risk_metrics.to_csv("data\\processed\\var_cvar_report.csv", index=False)


#rolling 90 day sharpee ratio
import matplotlib.pyplot as plt
import numpy as np
df['daily_return'] = (df.groupby('amfi_code')['nav'].pct_change())
df['date'] = pd.to_datetime(df['date'])


# Select first 5 funds
top5 = df['amfi_code'].unique()[:5]

plt.figure(figsize=(18,8))

# Calculate and plot Rolling Sharpe Ratio
for fund in top5:

    # Get data for one fund
    temp = df[df['amfi_code'] == fund].copy()

    # Calculate Rolling 90-Day Sharpe Ratio
    temp['rolling_sharpe'] = (
        temp['daily_return'].rolling(90).mean()
        /
        temp['daily_return'].rolling(90).std()
    ) * np.sqrt(252)

    # Plot
    plt.plot(temp['date'], temp['rolling_sharpe'], label=fund)

# Graph settings
plt.title("Rolling 90-Day Sharpe Ratio")
plt.xlabel("Date")
plt.ylabel("Sharpe Ratio")
plt.legend(title="AMFI Code")
plt.grid(True)
plt.xticks(rotation=45)


plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("data\\processed\\rolling_sharpe_chart.png")

plt.show()

#Cohort Analysis
import pandas as pd
import matplotlib.pyplot as plt
df=pd.read_csv("data\\processed\\clean_investor_transaction.csv")
df["transaction_date"] = pd.to_datetime(df["transaction_date"])
df['year'] = df['transaction_date'].dt.year
firstyear=(df.groupby("investor_id")['year'].min().reset_index())
firstyear.columns = ['investor_id', 'cohort']

# Add cohort back to transaction data
df = df.merge(firstyear, on='investor_id')

#Avg sip by cohort
sip = df[df['transaction_type'] == 'SIP']

avg_sip = (
    sip.groupby('cohort')['amount_inr']
       .mean()
       .reset_index()
)

print(avg_sip)
#total investment by cohort
total_investment = (
    df.groupby('cohort')['amount_inr']
      .sum()
      .reset_index()
)

print(total_investment)
#fav_fund
fund_pref = (
    df.groupby(['cohort', 'amfi_code'])
      .size()
      .reset_index(name='count')
)
#fav_fund

fav_fund = (
    fund_pref.sort_values('count', ascending=False)
             .drop_duplicates('cohort')
)

print(fav_fund)

# Merge Average SIP and Total Investment
cohort_analysis = pd.merge(
    avg_sip,
    total_investment,
    on="cohort",
    how="outer"
)

# Merge Favourite Fund
cohort_analysis = pd.merge(
    cohort_analysis,
    fav_fund,
    on="cohort",
    how="outer"
)

# Rename columns for better readability
cohort_analysis.columns = [
    "Cohort",
    "Average_SIP_Amount",
    "Total_Investment",
    "AMFI_Code",
    "Fund_Count"
]

# Display
print(cohort_analysis)

# Save as CSV
cohort_analysis.to_csv("cohort_analysis.csv", index=False)

print("CSV saved successfully!")

#SIP continuation analysis
import pandas as pd
import matplotlib.pyplot as plt
df=pd.read_csv("data\\processed\\clean_investor_transaction.csv")
df["transaction_date"] = pd.to_datetime(df["transaction_date"])
df=df[df["transaction_type"]=="SIP"]
df=df.sort_values(['investor_id', 'transaction_date'])
df["gap_days"]= df.groupby('investor_id')['transaction_date'].diff().dt.days
count=df.groupby('investor_id').size().reset_index(name='sip_count') 
# Keep investors with 6 or more SIPs
eligible = count[count['sip_count'] >= 6]

# Filter only eligible investors
sip = df.merge(eligible[['investor_id']], on='investor_id')

# Calculate average gap
result = sip.groupby('investor_id')['gap_days'].mean().reset_index()

# Add SIP count
result = result.merge(eligible, on='investor_id')

# Flag investors
result['status'] = result['gap_days'].apply(
    lambda x: 'At-Risk' if x > 35 else 'Active'
)

# Rename columns
result.rename(columns={
    'investor_id': 'Investor_ID',
    'gap_days': 'Average_Gap_Days',
    'sip_count': 'SIP_Transactions',
    'status': 'Investor_Status'
}, inplace=True)

# Display result
print(result)

# Save to CSV
result.to_csv("sip_continuity.csv", index=False)

print("CSV Saved Successfully!")

# Sector concentration analysis
import pandas as pd

# Load portfolio holdings
df = pd.read_csv("data\\raw\\09_portfolio_holdings.csv")

# Calculate HHI
hhi = df.groupby('amfi_code')['weight_pct'].apply(lambda x: (x**2).sum()).reset_index()

# Rename column
hhi.columns = ['amfi_code', 'HHI']

# Classify portfolio concentration
hhi['Portfolio_Type'] = hhi['HHI'].apply(
    lambda x: 'Highly Concentrated' if x > 2500
    else 'Moderately Concentrated' if x > 1500
    else 'Diversified'
)

# Display result
print(hhi)

# Save to CSV
hhi.to_csv("sector_hhi.csv", index=False)

print("Sector HHI saved successfully!")

import matplotlib.pyplot as plt

# Sort by HHI
hhi = hhi.sort_values(by='HHI', ascending=False)

plt.figure(figsize=(10,6))

plt.barh(hhi['amfi_code'].astype(str), hhi['HHI'])

plt.xlabel("HHI")
plt.ylabel("AMFI Code")
plt.title("Sector Concentration (HHI) by Fund")

plt.gca().invert_yaxis()   # Highest HHI at the top

plt.tight_layout()
plt.savefig("sector_hhi_chart.png")
plt.show()
