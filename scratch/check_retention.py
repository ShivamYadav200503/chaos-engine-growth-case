import os
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["OMP_NUM_THREADS"] = "1"

import pandas as pd

cr = pd.read_csv('data/processed/GameA_creatives_clean.csv')
cat = pd.read_csv('data/raw/GameA_creatives_catalog.csv')

# Check date range of mature cohorts
mature = cr[cr['date'] <= '2025-08-31'].copy()
print("Total rows:", len(cr), "Mature rows:", len(mature))
print("Mature installs sum:", mature['installs_mmp'].sum(), "cohort_installs sum:", mature['cohort_installs'].sum())
print("retained_d1 sum:", mature['retained_d1'].sum(), "retained_d7 sum:", mature['retained_d7'].sum())

# Net-D attribution fix check
print("\nBefore Net-D fix:")
print(cr[cr['network'] == 'Net-D'][['date', 'creative_id', 'cost', 'impressions_network_reported', 'installs_mmp']].head(10))
