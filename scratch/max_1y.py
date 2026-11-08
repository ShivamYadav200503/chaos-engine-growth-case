import numpy as np, pandas as pd
from scipy.optimize import minimize
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from src.config import *

df = pd.read_csv('outputs/tables/q1_gameA_cell_values.csv')
active = df[(df['status']=='Active') & (~df['country_cell'].isin(['TOTAL', 'all countries except United States']))].copy().reset_index(drop=True)
s0 = active['baseline_weekly_spend'].values * 12.0
r1y = active['predicted_1y_roas'].values
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

constraints = [
    {'type': 'eq', 'fun': lambda x: (s0 * x).sum() - 250000.0},
    {'type': 'ineq', 'fun': lambda x: (s0[net_a_idx] * x[net_a_idx]).sum() - 0.40 * net_a_base}
]

obj = lambda x: -(s0 * x * r1y * (np.clip(x, 0.5, 2.0)**(-k)) * HOLIDAY_FACTOR).sum()
x0 = np.full(n, 250000.0 / s0.sum())
x0 = np.clip(x0, [b[0] for b in bounds], [b[1] for b in bounds])
x0 = x0 * (250000.0 / (s0 * x0).sum())

res = minimize(obj, x0, method='SLSQP', bounds=bounds, constraints=constraints)
spend = (s0 * res.x).sum()
rev1y = -res.fun
print(f"Max 1Y Rev at 250k: {rev1y:,.2f} | 1Y ROAS: {rev1y/spend:.4f}")

