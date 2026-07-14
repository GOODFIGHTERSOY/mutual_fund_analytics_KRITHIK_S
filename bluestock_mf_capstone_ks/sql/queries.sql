--TOP 5 FUNDS BY AUM
SELECT fund_name, aum from fact_performance ORDER BY aum DESC LIMIT 5;


--Average NAV per month
SELECT
strftime('%Y-%m', nav_date) AS month,
ROUND(AVG(nav), 2) AS avg_nav
FROM fact_nav
GROUP BY month
ORDER BY month;

--SIP INFLOW
SELECT
strftime('%Y', transaction_date) AS year,
SUM(amount) AS sip_inflow
FROM fact_transactions
WHERE transaction_type = 'SIP'
GROUP BY year
ORDER BY year;

--Transactions by state
SELECT
state,
COUNT(*) AS total_transactions,
SUM(amount) AS total_amount
FROM fact_transactions
GROUP BY state
ORDER BY total_amount DESC;

--funds with expense ration less than 1%
SELECT
d.scheme_name,
p.expense_ratio
FROM fact_performance p
JOIN dim_fund d
ON p.amfi_code = d.amfi_code
WHERE p.expense_ratio < 1
ORDER BY p.expense_ratio;