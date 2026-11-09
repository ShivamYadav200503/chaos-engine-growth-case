import os
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["OMP_NUM_THREADS"] = "1"

import pandas as pd

cols = [
    'date', 'platform', 'country', 'network', 'campaign_id', 'creative_id',
    'installs_mmp', 'cost', 'impressions_network_reported', 'clicks_network_reported',
    'cohort_installs', 'retained_d1', 'retained_d7',
    'ad_rev_d7_clean', 'iap_rev_d7_clean', 'ad_rev_d30_clean', 'iap_rev_d30_clean'
]

chunks = []
for chunk in pd.read_csv('data/processed/GameA_creatives_clean.csv', usecols=cols, chunksize=10000):
    chunks.append(chunk)

cr = pd.concat(chunks, ignore_index=True)
print("Loaded successfully! Rows:", len(cr))

# Let's inspect Net-D
net_d = cr[cr['network'] == 'Net-D']
print("\nNet-D creative_ids:", net_d['creative_id'].value_counts())
print("\nNet-D summary by creative_id:")
print(net_d.groupby('creative_id').agg({
    'cost': 'sum',
    'impressions_network_reported': 'sum',
    'clicks_network_reported': 'sum',
    'installs_mmp': 'sum',
    'cohort_installs': 'sum',
    'retained_d1': 'sum',
    'retained_d7': 'sum',
    'ad_rev_d7_clean': 'sum',
    'iap_rev_d7_clean': 'sum',
    'ad_rev_d30_clean': 'sum',
    'iap_rev_d30_clean': 'sum',
}))
