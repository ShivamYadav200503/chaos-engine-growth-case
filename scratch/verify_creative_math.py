import os
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["OMP_NUM_THREADS"] = "1"

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

import numpy as np
import pandas as pd
from src.config import CREATIVE_WEAROUT, PLAN_WEEKS, EXISTING_CREATIVE_CARRY_WEEKS, NEW_CREATIVE_WEEKS

# Load plan.csv
plan = pd.read_csv('submission/plan.csv')
cells = plan[plan['network'] != 'TOTAL']

# Network spend in CFO plan
spend_by_net = cells.groupby('network')['quarter_spend'].sum().to_dict()
print("Quarter Spend by Network in CFO Plan:")
for net, sp in spend_by_net.items():
    print(f"  {net}: ${sp:,.2f}")

# Imps per dollar from September baseline
cr = pd.read_csv('data/processed/GameA_creatives_clean.csv')
sep_cr = cr[(cr['date'] >= '2025-09-01') & (cr['date'] <= '2025-09-28')]
summary = sep_cr.groupby('network').agg({
    'impressions_network_reported': 'sum',
    'cost': 'sum'
}).reset_index()
summary['imps_per_dollar'] = summary['impressions_network_reported'] / summary['cost']
imps_per_dollar = summary.set_index('network')['imps_per_dollar'].to_dict()

# Calculate quarterly impressions
quarter_imps = {}
new_period_imps = {}
creatives_needed = {}

for net in ['Net-A', 'Net-B', 'Net-C', 'Net-D']:
    sp = spend_by_net.get(net, 0)
    ipd = imps_per_dollar.get(net, 0)
    tot_imps = sp * ipd
    new_imps = tot_imps * (NEW_CREATIVE_WEEKS / PLAN_WEEKS)
    max_cap = CREATIVE_WEAROUT[net]['max_impressions']
    num_cr = int(np.ceil(new_imps / max_cap))
    
    quarter_imps[net] = tot_imps
    new_period_imps[net] = new_imps
    creatives_needed[net] = num_cr
    
    print(f"\n{net}:")
    print(f"  Total Spend: ${sp:,.2f} | Imps/dollar: {ipd:.2f}")
    print(f"  Total Quarter Imps: {tot_imps:,.0f} ({tot_imps/12:,.0f} / wk)")
    print(f"  Weeks 3-12 Imps: {new_imps:,.0f}")
    print(f"  Max Imps/creative: {max_cap:,.0f}")
    print(f"  New Creatives Required: {num_cr}")

