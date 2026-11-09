import os
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["MPLCONFIGDIR"] = "scratch/mpl_cache"

import sys
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

raw_tel_a = pd.read_csv("data/raw/GameA_telemetry_daily.csv")
clean_tel_a = pd.read_csv("data/processed/GameA_telemetry_clean.csv")

raw_tel_a["ad_rev"] = raw_tel_a["banner_rev"] + raw_tel_a["interstitial_rev"] + raw_tel_a["rewarded_rev"]
clean_tel_a["ad_rev"] = clean_tel_a["banner_rev"] + clean_tel_a["interstitial_rev"] + clean_tel_a["rewarded_rev"]

sub_dates = (raw_tel_a["date"] >= "2025-07-08") & (raw_tel_a["date"] <= "2025-07-22")
g_raw = raw_tel_a[sub_dates].groupby("date")["ad_rev"].sum()
g_clean = clean_tel_a[sub_dates].groupby("date")["ad_rev"].sum()

print("Raw vs Clean ad rev July 8-22:")
print(pd.DataFrame({"Raw": g_raw, "Clean": g_clean}))

# Check cohorts ad_rev_all_sources ratio
raw_coh_a = pd.read_csv("data/raw/GameA_cohorts.csv")
print("\nCohorts columns:")
for c in raw_coh_a.columns:
    if "all_sources" in c or "iap_rev" in c or "ad_rev" in c:
        print(" ", c)

