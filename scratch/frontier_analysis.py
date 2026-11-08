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

def evaluate_allocation(x):
    spend = s0 * x
    x_clip = np.clip(x, MIN_GAIN_MULTIPLIER, MAX_CELL_MULTIPLIER)
    roas_factor = (x_clip ** (-k)) * HOLIDAY_FACTOR
    
    d120_roas = r0_d120 * roas_factor
    d120_rev = spend * d120_roas
    
    r1y_roas = r0_1y * roas_factor
    r1y_rev = spend * r1y_roas
    
    cpi_factor = (x_clip ** (0.7 * k)) / HOLIDAY_FACTOR
    cpi = cpi0 * cpi_factor
    installs = spend / cpi
    
    # Organic uplift
    k_organic = 0.0485
    organic_ltv_d120 = 2.0516
    organic_ltv_1y = 2.45  # estimated 1y organic LTV
    organic_installs = installs * k_organic
    organic_d120_rev = organic_installs * organic_ltv_d120
    organic_1y_rev = organic_installs * organic_ltv_1y
    
    tot_spend = spend.sum()
    tot_paid_installs = installs.sum()
    tot_org_installs = organic_installs.sum()
    tot_all_installs = tot_paid_installs + tot_org_installs
    
    tot_d120_rev = d120_rev.sum()
    tot_d120_rev_with_org = tot_d120_rev + organic_d120_rev.sum()
    
    tot_1y_rev = r1y_rev.sum()
    tot_1y_rev_with_org = tot_1y_rev + organic_1y_rev.sum()
    
    return {
        "spend": tot_spend,
        "installs": tot_paid_installs,
        "org_installs": tot_org_installs,
        "total_installs": tot_all_installs,
        "d120_rev": tot_d120_rev,
        "d120_roas": tot_d120_rev / tot_spend,
        "d120_rev_org": tot_d120_rev_with_org,
        "d120_roas_org": tot_d120_rev_with_org / tot_spend,
        "1y_rev": tot_1y_rev,
        "1y_roas": tot_1y_rev / tot_spend,
        "1y_rev_org": tot_1y_rev_with_org,
        "1y_roas_org": tot_1y_rev_with_org / tot_spend,
        "x": x,
    }

# Test across budgets
budgets = [75000, 100000, 120000, 140000, 160000, 182325, 200000, 220000, 250000, 300000, 350000]
results = []

for b in budgets:
    constraints = [
        {"type": "eq", "fun": lambda x, target=b: (s0 * x).sum() - target},
        {"type": "ineq", "fun": lambda x: (s0[net_a_indices] * x[net_a_indices]).sum() - MIN_LINE_MULTIPLIER * net_a_base_spend},
    ]
    # Maximize D120 revenue
    obj = lambda x: -(s0 * x * r0_d120 * (np.clip(x, MIN_GAIN_MULTIPLIER, MAX_CELL_MULTIPLIER) ** (-k)) * HOLIDAY_FACTOR).sum()
    
    # Smart initial guess: give priority to higher ROAS cells
    x0 = np.full(n_cells, b / s0.sum())
    x0 = np.clip(x0, [bnd[0] for bnd in bounds], [bnd[1] for bnd in bounds])
    x0 = x0 * (b / (s0 * x0).sum())
    
    res = minimize(obj, x0, method="SLSQP", bounds=bounds, constraints=constraints,
                   options={"maxiter": 1000, "ftol": 1e-9})
    
    metrics = evaluate_allocation(res.x)
    results.append({
        "budget": b,
        "spend": metrics["spend"],
        "installs": metrics["installs"],
        "d120_rev": metrics["d120_rev"],
        "d120_roas": metrics["d120_roas"],
        "d120_roas_org": metrics["d120_roas_org"],
        "1y_rev": metrics["1y_rev"],
        "1y_roas": metrics["1y_roas"],
        "1y_roas_org": metrics["1y_roas_org"],
        "cfo_compliant": metrics["d120_roas"] >= 1.00,
        "cfo_compliant_org": metrics["d120_roas_org"] >= 1.00,
    })

res_df = pd.DataFrame(results)
print(res_df.to_string())

