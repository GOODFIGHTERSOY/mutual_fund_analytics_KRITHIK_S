create table dim_fund(amfi_code varchar(50) primary key,fund_house text,scheme_name text,category text,sub_category text,risk_grade text);
create table fact_nav(amfi_code varchar(50) primary key ,nav_date date,nav real,daily_return real,foreign key(amfi_code) references dim_fund(amfi_code));
create table fact_transactions(transaction_id INTEGER PRIMARY KEY,investor_id TEXT,amfi_code varchar(50),transaction_date DATE,transaction_type TEXT,
amount REAL,
units REAL,
FOREIGN KEY (amfi_code)
REFERENCES dim_fund(amfi_code)
);

create table fact_performance( amfi_code varchar(50),scheme_name text,fund_house text,category text,plan text,
return_1y REAL,
return_3y REAL,
return_5y REAL,
volatility REAL,
sharpe_ratio REAL,
expense_ratio REAL,
PRIMARY KEY (amfi_code),
FOREIGN KEY (amfi_code)
REFERENCES dim_fund(amfi_code)
);