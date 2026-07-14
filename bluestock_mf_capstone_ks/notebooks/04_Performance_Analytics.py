import pandas as pd
import matplotlib.pyplot as plt
df=pd.read_csv("data\\processed\\clean_nav.csv")

Nav=df.sort_values(["amfi_code","date"])
print(Nav.head())

#pct_change calculates the percentage change between the current and a prior element.
Nav["daily_return"]=(Nav.groupby("amfi_code")["nav"].pct_change())

print(Nav[["amfi_code","date","nav","daily_return"]].head())

#Annualized returns
annual_returns = (
    Nav.groupby("amfi_code")["daily_return"].apply(lambda x:((1 + x.dropna()).prod())**(252 / len(x.dropna()))- 1).reset_index())

annual_returns.columns = ["amfi_code","annualized_return"]

annual_returns["annualized_return"] = (
    annual_returns["annualized_return"] * 100
)

print(annual_returns.head())

final_df = pd.merge(
    Nav,
    annual_returns,
    on="amfi_code",
    how="left"
)

final_df.to_csv("data/processed/returns_computed.csv",index=False)


selected_funds = [
    "119551",  # SBI Bluechip
    "125497",  # HDFC Top 100
    "120503",  # ICICI Bluechip
    "119092",  # Axis Bluechip
    "120841"   # Kotak Bluechip
]
Nav["date"] = pd.to_datetime(Nav["date"])

results = []
def calculate_cagr(fund, years):

    end_date = fund["date"].max()

    start_date = end_date - pd.DateOffset(years=years)

    historical = fund[fund["date"] <= start_date]

    if historical.empty:
        return None

    start_nav = historical.iloc[-1]["nav"]

    end_nav = fund.iloc[-1]["nav"]

    cagr = ((end_nav / start_nav) ** (1 / years)) - 1

    return round(cagr * 100, 2)

for code in selected_funds:

    fund = Nav[
        Nav["amfi_code"].astype(str) == code
    ].sort_values("date")

    results.append({
        "amfi_code": code,
        "CAGR_1Y": calculate_cagr(fund, 1),
        "CAGR_3Y": calculate_cagr(fund, 3),
        "CAGR_5Y": calculate_cagr(fund, 5)
    })

cagr_df = pd.DataFrame(results)

print(cagr_df)

cagr_df.to_csv("reports\\cagr_report.csv")


#sharpe ratio
import pandas as pd
import numpy as np

RF = 0.065   # 6.5%

sharpe_results = []

for code, fund in Nav.groupby("amfi_code"):

    returns = fund["daily_return"].dropna()

    if len(returns) == 0:
        continue

    annual_return = returns.mean() * 252

    annual_volatility = returns.std() * np.sqrt(252)

    sharpe = (
        (annual_return - RF)
        / annual_volatility
    )

    sharpe_results.append({
        "amfi_code": code,
        "annual_return": annual_return * 100,
        "annual_volatility": annual_volatility * 100,
        "sharpe_ratio": round(sharpe, 3)
    })

sharpe_df = pd.DataFrame(sharpe_results)

print(sharpe_df)
sharpe_df.to_csv("reports\\sharpe_values.csv")


#sortino values
import pandas as pd
import numpy as np

RF = 0.065   # 6.5%

sortino_results = []

for code, fund in Nav.groupby("amfi_code"):

    returns = fund["daily_return"].dropna()

    if len(returns) == 0:
        continue

    # Annualized return
    annual_return = returns.mean() * 252

    # Only negative returns
    downside_returns = returns[returns < 0]

    if len(downside_returns) == 0:
        downside_std = np.nan
    else:
        downside_std = (
            downside_returns.std()
            * np.sqrt(252)
        )

    if downside_std == 0 or pd.isna(downside_std):
        sortino = np.nan
    else:
        sortino = (
            (annual_return - RF)
            / downside_std
        )

    sortino_results.append({
        "amfi_code": code,
        "annual_return": round(annual_return * 100, 2),
        "downside_risk": round(downside_std * 100, 2) if pd.notna(downside_std) else np.nan,
        "sortino_ratio": round(sortino, 3) if pd.notna(sortino) else np.nan
    })

sortino_df = pd.DataFrame(sortino_results)

print(sortino_df)
sortino_df.to_csv("reports\\sortino_values.csv")


#Alpha beta vs benchmark
import pandas as pd

nifty = pd.read_csv("data\\raw\\10_benchmark_indices.csv")
nifty100 = nifty[nifty["index_name"] == "NIFTY100"]

nifty100["date"] = pd.to_datetime(nifty100["date"])

nifty100["benchmark_return"] = nifty100["close_value"].pct_change()

nifty100 = nifty100.dropna()

Nav["date"] = pd.to_datetime(Nav["date"])

Nav = Nav.sort_values(
    ["amfi_code", "date"]
)

Nav["daily_return"] = (
    Nav.groupby("amfi_code")["nav"]
    .pct_change()
)

from scipy.stats import linregress
import pandas as pd

results = []

for code, fund in Nav.groupby("amfi_code"):

    merged = pd.merge(
        fund,
        nifty100,
        on="date",
        how="inner"
    )

    merged = merged.dropna(
        subset=["daily_return", "benchmark_return"]
    )

    if len(merged) < 30:
        continue

    regression = linregress(
        merged["benchmark_return"],
        merged["daily_return"]
    )

    beta = regression.slope

    alpha = regression.intercept * 252

    results.append({
        "amfi_code": code,
        "alpha": round(alpha, 4),
        "beta": round(beta, 4),
        "r_squared": round(regression.rvalue**2, 4)
    })

alpha_beta_df = pd.DataFrame(results)

print(alpha_beta_df)

alpha_beta_df.to_csv("reports\\alpha_beta_values.csv", index=False)

#Maximum drawdown 
import pandas as pd

Nav["date"] = pd.to_datetime(Nav["date"])

Nav = Nav.sort_values(
    ["amfi_code", "date"]
)

results = []

for code, fund in Nav.groupby("amfi_code"):

    fund = fund.sort_values("date").copy()

    # Running maximum NAV
    fund["running_max"] = fund["nav"].cummax()

    # Drawdown
    fund["drawdown"] = (
        fund["nav"] / fund["running_max"]
    ) - 1

    # Maximum drawdown
    max_dd = fund["drawdown"].min()

    # Worst day
    worst_idx = fund["drawdown"].idxmin()

    worst_date = fund.loc[
        worst_idx,
        "date"
    ]

    results.append({
        "amfi_code": code,
        "max_drawdown": round(max_dd * 100, 2),
        "worst_date": worst_date
    })

mdd_df = pd.DataFrame(results)

print(mdd_df)

mdd_df.to_csv("reports\\max_drawdown.csv", index=False)


#Fund Scorecard

import pandas as pd
cagr_df["amfi_code"] = cagr_df["amfi_code"].astype(str)

sharpe_df["amfi_code"] = sharpe_df["amfi_code"].astype(str)

alpha_beta_df["amfi_code"] = alpha_beta_df["amfi_code"].astype(str)

mdd_df["amfi_code"] = mdd_df["amfi_code"].astype(str)

fund_master = pd.read_csv("data\\processed\\fund_master_clean.csv")
fund_master["amfi_code"] = fund_master["amfi_code"].astype(str)
print("cagr_df:", cagr_df["amfi_code"].dtype)
print("sharpe_df:", sharpe_df["amfi_code"].dtype)
print("alpha_beta_df:", alpha_beta_df["amfi_code"].dtype)
print("mdd_df:", mdd_df["amfi_code"].dtype)
print("fund_master:", fund_master["amfi_code"].dtype)
print(cagr_df.columns.tolist())
print(sharpe_df.columns.tolist())
print(alpha_beta_df.columns.tolist())
print(mdd_df.columns.tolist())
print(fund_master.columns.tolist())


cagr = cagr_df[["amfi_code", "CAGR_3Y"]].copy()

sharpe = sharpe_df[["amfi_code", "sharpe_ratio"]].copy()

alpha = alpha_beta_df[["amfi_code", "alpha"]].copy()

mdd = mdd_df[["amfi_code", "max_drawdown"]].copy()

expense = fund_master[["amfi_code", "expense_ratio_pct"]].copy()

#Merging all the dataframes to create a comprehensive scorecard

scorecard = cagr.merge(
    sharpe,
    on="amfi_code",
    how="left"
)

scorecard = scorecard.merge(
    alpha,
    on="amfi_code",
    how="left"
)

scorecard = scorecard.merge(
    mdd,
    on="amfi_code",
    how="left"
)

scorecard = scorecard.merge(
    expense,
    on="amfi_code",
    how="left"
)

#Removing duplicates

scorecard = scorecard.loc[:, ~scorecard.columns.duplicated()]

#Ranks

# Higher is better

scorecard["return_rank"] = (
    scorecard["CAGR_3Y"]
    .rank(ascending=False)
)

scorecard["sharpe_rank"] = (
    scorecard["sharpe_ratio"]
    .rank(ascending=False)
)

scorecard["alpha_rank"] = (
    scorecard["alpha"]
    .rank(ascending=False)
)

# Lower is better

scorecard["expense_rank"] = (
    scorecard["expense_ratio_pct"]
    .rank(ascending=True)
)

scorecard["dd_rank"] = (
    scorecard["max_drawdown"]
    .rank(ascending=True)
)

#Converting ranks to scores (0-100 scale)

n = len(scorecard)

scorecard["return_score"] = (
    (n - scorecard["return_rank"])
    / (n - 1)
) * 100

scorecard["sharpe_score"] = (
    (n - scorecard["sharpe_rank"])
    / (n - 1)
) * 100

scorecard["alpha_score"] = (
    (n - scorecard["alpha_rank"])
    / (n - 1)
) * 100

scorecard["expense_score"] = (
    (n - scorecard["expense_rank"])
    / (n - 1)
) * 100

scorecard["dd_score"] = (
    (n - scorecard["dd_rank"])
    / (n - 1)
) * 100

#Fund score calculation based on weighted average of individual scores

scorecard["fund_score"] = (

      0.30 * scorecard["return_score"]
    + 0.25 * scorecard["sharpe_score"]
    + 0.20 * scorecard["alpha_score"]
    + 0.15 * scorecard["expense_score"]
    + 0.10 * scorecard["dd_score"]

)

#sorting

scorecard = scorecard.sort_values(
    "fund_score",
    ascending=False
)

#Top 10 funds based on fund score

print("\nTop 10 Funds\n")

print(
    scorecard[
        [
            "amfi_code",
            "CAGR_3Y",
            "sharpe_ratio",
            "alpha",
            "expense_ratio_pct",
            "max_drawdown",
            "fund_score"
        ]
    ].head(10)
)

#Saving the scorecard to a CSV file

scorecard.to_csv(
    "reports/fund_scorecard.csv",
    index=False
)

print("\nFund scorecard saved successfully!")


top5 = scorecard.nlargest(5, "fund_score")

top_codes = top5["amfi_code"].astype(str).tolist()

print(top_codes)


Nav["nav_date"] = pd.to_datetime(Nav["date"])

nav = Nav.sort_values(
    ["amfi_code", "nav_date"]
)

nav["daily_return"] = (
    nav.groupby("amfi_code")["nav"]
    .pct_change()
)

end_date = nav["nav_date"].max()

start_date = end_date - pd.DateOffset(years=3)

nav_3y = nav[nav["nav_date"] >= start_date]

# Nifty 50
nifty=pd.read_csv("data\\raw\\10_benchmark_indices.csv")
nifty50 = nifty[nifty["index_name"] == "NIFTY50"]
nifty50["date"] = pd.to_datetime(nifty50["date"])

nifty50 = nifty50.sort_values("date")

nifty50["benchmark_return"] = (
    nifty50["close_value"]
    .pct_change()
)

#NIFTY 100
nifty100 = nifty[nifty["index_name"] == "NIFTY100"]
nifty100["date"] = pd.to_datetime(nifty100["date"])

nifty100 = nifty100.sort_values("date")

nifty100["benchmark_return"] = (
    nifty100["close_value"]
    .pct_change()
)

#Comparison chart
import matplotlib.pyplot as plt

plt.figure(figsize=(15,8))

for code in top_codes:

    fund = nav_3y[
        nav_3y["amfi_code"].astype(str) == code
    ].copy()

    fund["cum_return"] = (
        1 + fund["daily_return"]
    ).cumprod()

    plt.plot(
        fund["nav_date"],
        fund["cum_return"],
        label=f"Fund {code}"
    )

# Nifty 50

nifty50["cum_return"] = (
    1 + nifty50["benchmark_return"]
).cumprod()

plt.plot(
    nifty50["date"],
    nifty50["cum_return"],
    linewidth=3,
    linestyle="--",
    label="Nifty 50"
)

# Nifty 100

nifty100["cum_return"] = (
    1 + nifty100["benchmark_return"]
).cumprod()

plt.plot(
    nifty100["date"],
    nifty100["cum_return"],
    linewidth=3,
    linestyle=":",
    label="Nifty 100"
)

plt.title(
    "Top 5 Funds vs Nifty 50 & Nifty 100 (3 Years)"
)

plt.xlabel("Date")
plt.ylabel("Growth of ₹1 Investment")

plt.legend(
    bbox_to_anchor=(1.05,1),
    loc="upper left"
)

plt.tight_layout()

plt.savefig(
    "reports/benchmark_chart.png",
    dpi=300
)

plt.show()
