import os
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["OMP_NUM_THREADS"] = "1"

import pandas as pd

df = pd.read_csv('data/processed/GameA_creatives_clean.csv')
print("Total rows:", len(df))
print("\nUnique networks:", df['network'].unique())

print("\nBreakdown by network and creative_id (top spend / impressions / installs):")
agg = df.groupby(['network', 'creative_id'], as_index=False).agg({
    'cost': 'sum',
    'impressions_network_reported': 'sum',
    'clicks_network_reported': 'sum',
    'installs_mmp': 'sum'
})
print(agg.to_string())

print("\nNet-D rows:")
net_d = df[df['network'] == 'Net-D']
print("Net-D rows count:", len(net_d))
print(net_d.groupby('creative_id').agg({
    'cost': 'sum',
    'impressions_network_reported': 'sum',
    'clicks_network_reported': 'sum',
    'installs_mmp': 'sum',
    'ad_rev_d7_clean': 'sum',
    'iap_rev_d7_clean': 'sum',
    'ad_rev_d30_clean': 'sum',
    'iap_rev_d30_clean': 'sum',
}).to_string())
