import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

import numpy as np
import pandas as pd
import statsmodels.api as sm

# Load master clean
master = pd.read_csv("data/processed/GameA_master_clean.csv")
print("Columns:", master.columns.tolist())
print("Networks in master clean:", master["network"].unique().tolist())

# Group by install_date, network
daily_net = master.groupby(["install_date", "network"])["installs"].sum().unstack(fill_value=0).reset_index()
print("Columns in daily_net:", daily_net.columns.tolist())

# Paid networks vs Organic networks
paid_nets = ["Net-A", "Net-B", "Net-C", "Net-D"]
organic_nets = [c for c in daily_net.columns if c not in ["install_date"] + paid_nets]

daily_net["paid_installs"] = daily_net[paid_nets].sum(axis=1)
daily_net["organic_installs"] = daily_net[organic_nets].sum(axis=1)

print("\n--- Daily Totals Summary ---")
print(daily_net[["paid_installs", "organic_installs"]].describe())

daily_net["install_date"] = pd.to_datetime(daily_net["install_date"])
daily_net["day_of_week"] = daily_net["install_date"].dt.day_name()
daily_net["trend"] = np.arange(len(daily_net))

# Regression: organic_installs ~ paid_installs + day_of_week + trend
X = pd.get_dummies(daily_net["day_of_week"], drop_first=True, dtype=float)
X["trend"] = daily_net["trend"]
X["paid_installs"] = daily_net["paid_installs"]
X = sm.add_constant(X)
y = daily_net["organic_installs"]

model = sm.OLS(y, X).fit()
print("\n--- OLS Regression: Organic Installs ~ Paid Installs ---")
print(model.summary().tables[1])

# Also check with lags
X["paid_lag1"] = daily_net["paid_installs"].shift(1).fillna(method="bfill")
X["paid_lag2"] = daily_net["paid_installs"].shift(2).fillna(method="bfill")
model_lag = sm.OLS(y, X).fit()
print("\n--- OLS Regression with Lags ---")
print(model_lag.summary().tables[1])
