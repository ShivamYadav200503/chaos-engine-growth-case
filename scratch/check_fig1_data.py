import os
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["MPLCONFIGDIR"] = "scratch/mpl_cache"

import pandas as pd

raw_tel = pd.read_csv("data/raw/GameA_telemetry_daily.csv")
clean_tel = pd.read_csv("data/processed/GameA_telemetry_clean.csv")

print("Raw tel cols:", list(raw_tel.columns))
print("Clean tel cols:", list(clean_tel.columns))

# Group by date between 2025-07-08 and 2025-07-22
raw_sub = raw_tel[(raw_tel["date"] >= "2025-07-08") & (raw_tel["date"] <= "2025-07-22")]
clean_sub = clean_tel[(clean_tel["date"] >= "2025-07-08") & (clean_tel["date"] <= "2025-07-22")]

g_raw = raw_sub.groupby("date")["ad_rev_all_sources"].sum()
g_clean = clean_sub.groupby("date")["ad_rev_all_sources_clean"].sum()

comp = pd.DataFrame({"raw_ad_rev": g_raw, "clean_ad_rev": g_clean})
print("\nDaily Ad Rev July 8-22:")
print(comp)

