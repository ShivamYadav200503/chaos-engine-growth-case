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

bounds = []
for i in range(n_cells):
    if i in [net_b_and_idx, net_b_ios_idx, net_c_and_idx, net_d_and_idx]:
        bounds.append((MIN_LINE_MULTIPLIER, MAX_CELL_MULTIPLIER))
    else:
        bounds.append((0.0, MAX_CELL_MULTIPLIER))

def solve_max_spend_roas1(use_holiday=True, use_organic=False):
    h_factor = HOLIDAY_FACTOR if use_holiday else 1.0
    
    def eval_roas(x):
        spend = s0 * x
        x_clip = np.clip(x, MIN_GAIN_MULTIPLIER, MAX_CELL_MULTIPLIER)
        roas_factor = (x_clip ** (-k)) * h_factor
        d120_roas = r0_d120 * roas_factor
        d120_rev = spend * d120_roas
        
        if use_organic:
            cpi_factor = (x_clip ** (0.7 * k)) / h_factor
            cpi = cpi0 * cpi_factor
            installs = spend / cpi
            org_rev = installs * 0.0485 * 2.0516
            d120_rev += org_rev
            
        tot_spend = spend.sum()
        tot_rev = d120_rev.sum()
        return tot_rev / tot_spend if tot_spend > 0 else 0, tot_spend, tot_rev

    # Maximize spend subject to ROAS >= 1.0
    # Objective: -sum(spend)
    obj = lambda x: -(s0 * x).sum()
    
    constraints = [
        {"type": "ineq", "fun": lambda x: MAX_QUARTER_BUDGET - (s0 * x).sum()},
        {"type": "ineq", "fun": lambda x: (s0[net_a_indices] * x[net_a_indices]).sum() - MIN_LINE_MULTIPLIER * net_a_base_spend},
        {"type": "ineq", "fun": lambda x: eval_roas(x)[0] - 1.00},
    ]
    
    x0 = np.full(n_cells, 0.6)
    x0 = np.clip(x0, [b[0] for b in bounds], [b[1] for b in bounds])
    
    res = minimize(obj, x0, method="SLSQP", bounds=bounds, constraints=constraints,
                   options={"maxiter": 1000, "ftol": 1e-9})
    roas, sp, rev = eval_roas(res.x)
    return sp, rev, roas, res

for h, o in [(True, False), (True, True), (False, False), (False, True)]:
    sp, rev, roas, res = solve_max_spend_roas1(use_holiday=h, use_organic=o)
    print(f"Holiday={h}, Organic={o} -> Max Spend: ${sp:,.2f} | D120 Rev: ${rev:,.2f} | D120 ROAS: {roas:.4f} (Success: {res.success})")

