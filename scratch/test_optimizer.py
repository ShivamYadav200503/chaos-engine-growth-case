import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

import numpy as np
import pandas as pd
from scipy.optimize import minimize

from src.config import (
    PLAN_WEEKS, MAX_QUARTER_BUDGET, CFO_TARGET_D120_ROAS,
    MIN_LINE_MULTIPLIER, MAX_CELL_MULTIPLIER, MIN_GAIN_MULTIPLIER,
    K_EXPONENTS, HOLIDAY_FACTOR
)

# Load Game A cell values from Q1
df = pd.read_csv("outputs/tables/q1_gameA_cell_values.csv")
active_df = df[(df["status"] == "Active") & 
               (~df["country_cell"].isin(["TOTAL", "all countries except United States"]))].copy().reset_index(drop=True)

active_df["k"] = active_df["network"].map(K_EXPONENTS)
w0 = active_df["baseline_weekly_spend"].values
s0 = w0 * PLAN_WEEKS  # 12-week baseline spend per cell
r0_d120 = active_df["predicted_d120_roas"].values
r0_1y = active_df["predicted_1y_roas"].values
cpi0 = active_df["baseline_cpi"].values
k = active_df["k"].values
n_cells = len(active_df)

net_a_indices = active_df[active_df["network"] == "Net-A"].index.values
net_b_and_idx = active_df[(active_df["network"] == "Net-B") & (active_df["platform"] == "android")].index.values[0]
net_b_ios_idx = active_df[(active_df["network"] == "Net-B") & (active_df["platform"] == "ios")].index.values[0]
net_c_and_idx = active_df[(active_df["network"] == "Net-C") & (active_df["platform"] == "android")].index.values[0]
net_d_and_idx = active_df[(active_df["network"] == "Net-D") & (active_df["platform"] == "android")].index.values[0]

net_a_base_spend = s0[net_a_indices].sum()

def calc_all(x):
    spend = s0 * x
    x_clip = np.clip(x, MIN_GAIN_MULTIPLIER, MAX_CELL_MULTIPLIER)
    roas_factor = (x_clip ** (-k)) * HOLIDAY_FACTOR
    d120_roas = r0_d120 * roas_factor
    d120_rev = spend * d120_roas
    tot_spend = spend.sum()
    tot_d120_rev = d120_rev.sum()
    tot_d120_roas = tot_d120_rev / tot_spend if tot_spend > 0 else 0
    return tot_spend, tot_d120_rev, tot_d120_roas

# Max possible D120 ROAS at fixed spend levels
print("--- Maximum possible D120 ROAS at exact spend levels ---")
bounds = []
for i in range(n_cells):
    if i in [net_b_and_idx, net_b_ios_idx, net_c_and_idx, net_d_and_idx]:
        bounds.append((MIN_LINE_MULTIPLIER, MAX_CELL_MULTIPLIER))
    else:
        bounds.append((0.0, MAX_CELL_MULTIPLIER))

for target in [100000, 120000, 140000, 160000, 180000, 200000, 220000, 250000]:
    constraints = [
        {"type": "eq", "fun": lambda x, t=target: (s0 * x).sum() - t},
        {"type": "ineq", "fun": lambda x: (s0[net_a_indices] * x[net_a_indices]).sum() - MIN_LINE_MULTIPLIER * net_a_base_spend},
    ]
    # Maximize D120 ROAS (equivalent to maximizing D120 Rev at fixed spend)
    obj_fun = lambda x: -(s0 * x * r0_d120 * (np.clip(x, MIN_GAIN_MULTIPLIER, MAX_CELL_MULTIPLIER) ** (-k)) * HOLIDAY_FACTOR).sum()
    
    x0 = np.full(n_cells, target / s0.sum())
    x0 = np.clip(x0, [b[0] for b in bounds], [b[1] for b in bounds])
    # Adjust to sum to target
    x0 = x0 * (target / (s0 * x0).sum())
    
    res = minimize(obj_fun, x0, method="SLSQP", bounds=bounds, constraints=constraints,
                   options={"maxiter": 1000, "ftol": 1e-9})
    sp, rev, roas = calc_all(res.x)
    print(f"Target Spend: ${target:,.0f} -> Actual Spend: ${sp:,.2f} | Max D120 Rev: ${rev:,.2f} | Max D120 ROAS: {roas:.4f} (Success: {res.success})")
