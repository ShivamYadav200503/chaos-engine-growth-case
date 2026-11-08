import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

import numpy as np
import pandas as pd
from src.config import CREATIVE_WEAROUT, PLAN_WEEKS, EXISTING_CREATIVE_CARRY_WEEKS, NEW_CREATIVE_WEEKS

# Load the CFO plan spend by network
# Baseline weekly spend and impressions from September
cr = pd.read_csv('data/processed/GameA_creatives_clean.csv')
sep_cr = cr[(cr['date'] >= '2025-09-01') & (cr['date'] <= '2025-09-28')]
net_summary = sep_cr.groupby('network').agg({
    'impressions_network_reported': 'sum',
    'installs_mmp': 'sum',
    'cost': 'sum'
}).reset_index()

net_summary['cpm'] = net_summary['cost'] / (net_summary['impressions_network_reported'] / 1000.0)
net_summary['imps_per_dollar'] = net_summary['impressions_network_reported'] / net_summary['cost']

print("September Baseline CPM by Network:")
print(net_summary[['network', 'cost', 'impressions_network_reported', 'cpm', 'imps_per_dollar']])

