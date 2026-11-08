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

def solve_cfo_plan():
    # Find maximum spend such that portfolio D120 ROAS >= 1.0000
    # Let's do a binary search or precise grid search on budget, then optimize D120 rev
    low = 100000.0
    high = 160000.0
    best_res = None
    best_budget = low
    
    for _ in range(30):
        mid = (low + high) / 2.0
        constraints = [
            {"type": "eq", "fun": lambda x, target=mid: (s0 * x).sum() - target},
            {"type": "ineq", "fun": lambda x: (s0[net_a_indices] * x[net_a_indices]).sum() - MIN_LINE_MULTIPLIER * net_a_base_spend},
        ]
        obj = lambda x: -(s0 * x * r0_d120 * (np.clip(x, MIN_GAIN_MULTIPLIER, MAX_CELL_MULTIPLIER) ** (-k)) * HOLIDAY_FACTOR).sum()
        x0 = np.full(n_cells, mid / s0.sum())
        x0 = np.clip(x0, [bnd[0] for bnd in bounds], [bnd[1] for bnd in bounds])
        x0 = x0 * (mid / (s0 * x0).sum())
        
        res = minimize(obj, x0, method="SLSQP", bounds=bounds, constraints=constraints,
                       options={"maxiter": 1000, "ftol": 1e-9})
        
        spend = (s0 * res.x).sum()
        d120_rev = -res.fun
        roas = d120_rev / spend
        
        if roas >= 1.0000:
            best_res = res
            best_budget = mid
            low = mid
        else:
            high = mid
            
    return best_budget, best_res

b_opt, res_cfo = solve_cfo_plan()
spend = (s0 * res_cfo.x).sum()
x_clip = np.clip(res_cfo.x, MIN_GAIN_MULTIPLIER, MAX_CELL_MULTIPLIER)
d120_rev = (s0 * res_cfo.x * r0_d120 * (x_clip ** (-k)) * HOLIDAY_FACTOR).sum()
r1y_rev = (s0 * res_cfo.x * r0_1y * (x_clip ** (-k)) * HOLIDAY_FACTOR).sum()
cpi = cpi0 * (x_clip ** (0.7 * k)) / HOLIDAY_FACTOR
installs = ((s0 * res_cfo.x) / cpi).sum()

print(f"Optimal CFO Plan Spend: ${spend:,.2f}")
print(f"D120 Rev: ${d120_rev:,.2f} | D120 ROAS: {d120_rev/spend:.4f}")
print(f"1Y Rev: ${r1y_rev:,.2f} | 1Y ROAS: {r1y_rev/spend:.4f}")
print(f"Installs: {installs:,.0f}")
print(f"Net-A Line Spend: ${(s0[net_a_indices] * res_cfo.x[net_a_indices]).sum():,.2f} (Min: ${MIN_LINE_MULTIPLIER * net_a_base_spend:,.2f})")
print(f"Net-B And Spend: ${s0[net_b_and_idx] * res_cfo.x[net_b_and_idx]:,.2f} (Min: ${MIN_LINE_MULTIPLIER * s0[net_b_and_idx]:,.2f})")
print(f"Net-B iOS Spend: ${s0[net_b_ios_idx] * res_cfo.x[net_b_ios_idx]:,.2f} (Min: ${MIN_LINE_MULTIPLIER * s0[net_b_ios_idx]:,.2f})")
print(f"Net-C And Spend: ${s0[net_c_and_idx] * res_cfo.x[net_c_and_idx]:,.2f} (Min: ${MIN_LINE_MULTIPLIER * s0[net_c_and_idx]:,.2f})")
print(f"Net-D And Spend: ${s0[net_d_and_idx] * res_cfo.x[net_d_and_idx]:,.2f} (Min: ${MIN_LINE_MULTIPLIER * s0[net_d_and_idx]:,.2f})")

