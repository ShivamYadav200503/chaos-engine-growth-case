import os
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["OMP_NUM_THREADS"] = "1"

import pandas as pd

df = pd.read_csv('data/processed/GameA_creatives_clean.csv')
net_a = df[df['network'] == 'Net-A']

print("Net-A creative_id breakdown:")
print(net_a.groupby('creative_id').agg({
    'cost': 'sum',
    'impressions_network_reported': 'sum',
    'clicks_network_reported': 'sum',
    'installs_mmp': 'sum',
    'installs_network_reported': 'sum',
    'cohort_installs': 'sum',
    'ad_rev_d30_clean': 'sum',
    'iap_rev_d30_clean': 'sum',
}).to_string())

print("\nNet-A unknown date range and campaign_ids:")
net_a_unk = net_a[net_a['creative_id'] == 'unknown']
print("Dates min/max:", net_a_unk['date'].min(), net_a_unk['date'].max())
print("Campaign IDs in Net-A unknown:", net_a_unk['campaign_id'].value_counts())
print("Campaign IDs in Net-A known:", net_a[net_a['creative_id'] != 'unknown']['campaign_id'].value_counts())

ua_a = pd.read_csv('data/raw/GameA_ua_daily.csv')
net_a_ua = ua_a[ua_a['network'] == 'Net-A']
print("\nNet-A UA total cost:", net_a_ua['cost'].sum(), "installs:", net_a_ua['installs_mmp'].sum(), "imps:", net_a_ua['impressions'].sum())
print("Net-A creatives total cost:", net_a['cost'].sum(), "installs:", net_a['installs_mmp'].sum(), "imps:", net_a['impressions_network_reported'].sum())
