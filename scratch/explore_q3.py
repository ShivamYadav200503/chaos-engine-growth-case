import pandas as pd
import numpy as np

cr = pd.read_csv("data/processed/GameA_creatives_clean.csv")
cat = pd.read_csv("data/raw/GameA_creatives_catalog.csv")
ua = pd.read_csv("data/raw/GameA_ua_daily.csv")
plan = pd.read_csv("submission/plan.csv")

print("=== GAME A CREATIVES CATALOG ===")
for _, r in cat.iterrows():
    print(r['creative_id'], "|", r['network'], "|", r['creative_type'], "|", r['first_seen'], "|", r['last_seen'])

print("\n=== CREATIVES DAILY NETWORKS ===")
print(cr['network'].value_counts())

print("\n=== CREATIVE MERGE CHECK ===")
m = cr.merge(cat, on=["network", "creative_id"], how="left")
print("Null creative types:", m['creative_type'].isna().sum())
print(m.groupby(['network', 'creative_type'])['cost'].sum())
