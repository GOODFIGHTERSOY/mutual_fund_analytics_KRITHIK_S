#Fund recomendation
import pandas as pd

# Load performance data
df = pd.read_csv("data\\processed\\clean_performance.csv")

# Ask user for risk appetite
risk = input("Enter Risk Appetite (Low/Moderate/High): ")

# Filter matching risk grade
filtered = df[df['risk_grade'] == risk]

# Sort by Sharpe Ratio (Highest First)
recommendation = filtered.sort_values(
    by='sharpe_ratio',
    ascending=False
)

# Select Top 3 funds
top3 = recommendation.head(3)

# Display
print("\nTop 3 Recommended Funds\n")
print(top3[['amfi_code', 'risk_grade', 'sharpe_ratio']])

# Save as CSV
top3.to_csv("fund_recommendation.csv", index=False)

print("\nRecommendation saved successfully!")