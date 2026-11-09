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

df = pd.read_csv('data/processed/GameA_creatives_clean.csv', usecols=cols, engine='python')
print("Loaded successfully with engine='python'! Rows:", len(df))
print(df.head(2))
