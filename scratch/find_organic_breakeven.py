import numpy as np, pandas as pd
from scipy.optimize import minimize
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from src.config import *

df = pd.read_csv('outputs/tables/q1_gameA_cell_values.csv')
active = df[(df['status']=='Active') & (~df['country_cell'].isin(['TOTAL', 'all countries except United States']))].copy().reset_index(drop=True)
s0 = active['baseline_weekly_spend'].values * 12.0
r0_d120 = active['predicted_d120_roas'].values
r0_1y = active['predicted_1y_roas'].values
cpi0 = active['baseline_cpi'].values
k = active['network'].map(K_EXPONENTS).values
n = len(active)

net_a_idx = active[active['network']=='Net-A'].index.values
net_a_base = s0[net_a_idx].sum()

bounds = []
for i in range(n):
    if active.loc[i, 'network'] in ['Net-B', 'Net-C', 'Net-D']:
        bounds.append((0.40, 2.00))
    else:
        bounds.append((0.00, 2.00))

# Test grid of budgets from 135k to 170k with organic uplift
for b in np.arange(135000, 165000, 2500):
    constraints = [
        {'type': 'eq', 'fun': lambda x, target=b: (s0 * x).sum() - target},
        {'type': 'ineq', 'fun': lambda x: (s0[net_a_idx] * x[net_a_idx]).sum() - 0.40 * net_a_base}
    ]
    # Maximize D120 Rev with organic
    def obj(x):
        spend = s0 * x
        x_clip = np.clip(x, 0.5, 2.0)
        paid_rev = spend * r0_d120 * (x_clip**(-k)) * HOLIDAY_FACTOR
        cpi = cpi0 * (x_clip**(0.7*k)) / HOLIDAY_FACTOR
        installs = spend / cpi
        org_rev = installs * 0.0485 * 2.0516
        return -(paid_rev.sum() + org_rev.sum())

    x0 = np.full(n, b / s0.sum())
    x0 = np.clip(x0, [bnd[0] for bnd in bounds], [bnd[1] for bnd in bounds])
    x0 = x0 * (b / (s0 * x0).sum())

    res = minimize(obj, x0, method='SLSQP', bounds=bounds, constraints=constraints)
    spend = (s0 * res.x).sum()
    x_clip = np.clip(res.x, 0.5, 2.0)
    paid_rev = (spend * r0_d120 * (x_clip**(-k)) * HOLIDAY_FACTOR).sum()
    cpi = cpi0 * (x_clip**(0.7*k)) / HOLIDAY_FACTOR
    installs = (spend / cpi).sum()
    org_rev = (spend / cpi * 0.0485 * 2.0516).sum()
    tot_rev = paid_rev + org_rev
    print(f"Budget: ${b:,.0f} | Paid ROAS: {paid_rev/spend:.4f} | Blended ROAS (w/ Org): {tot_rev/spend:.4f}")

