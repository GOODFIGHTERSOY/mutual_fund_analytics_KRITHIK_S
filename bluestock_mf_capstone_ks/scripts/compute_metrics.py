import pandas as pd

df = pd.read_csv("data\\processed\\clean_nav.csv")

df['date'] = pd.to_datetime(df['date'])

df = df.sort_values(['amfi_code','date'])

# Daily Return
df['daily_return'] = df.groupby('amfi_code')['nav'].pct_change()

# Save
df.to_csv("data\\processed\\nav_metrics.csv", index=False)

print("Metrics Computed Successfully")