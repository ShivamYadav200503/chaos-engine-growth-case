import os
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["OMP_NUM_THREADS"] = "1"

import pandas as pd

cr = pd.read_csv("data/processed/GameA_creatives_clean.csv")
cat = pd.read_csv("data/raw/GameA_creatives_catalog.csv")

for net in ["Net-A", "Net-B", "Net-C", "Net-D"]:
    print(f"\n=== {net} Creatives in cr ===")
    sub = cr[cr["network"] == net]
    g = sub.groupby("creative_id").agg({
        "cost": "sum",
        "impressions_network_reported": "sum",
        "clicks_network_reported": "sum",
        "installs_mmp": "sum",
        "ad_rev_d30_clean": "sum",
        "iap_rev_d30_clean": "sum"
    })
    print(g)
