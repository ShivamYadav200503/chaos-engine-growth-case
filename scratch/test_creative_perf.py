import os
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["OMP_NUM_THREADS"] = "1"

import pandas as pd
import numpy as np

cr = pd.read_csv("data/processed/GameA_creatives_clean.csv")
cat = pd.read_csv("data/raw/GameA_creatives_catalog.csv")

print("cr shape:", cr.shape)
print("cat shape:", cat.shape)

# Let's inspect Net-D re-attribution
# On Net-D, rows with creative_id == 'unknown' have cost and impressions, while rows with creative_id == 'A-K029' have installs and revenues
net_d_mask = cr["network"] == "Net-D"
cr.loc[net_d_mask & (cr["creative_id"] == "unknown"), "creative_id"] = "A-K029"

# Re-group by date, network, creative_id, platform, country to merge the split rows
# Or just aggregate over the dataset
merged = cr.merge(cat[["creative_id", "creative_type"]], on="creative_id", how="left")
# For unknown or any unmerged, set creative_type
merged.loc[merged["creative_id"] == "A-K029", "creative_type"] = "store image (offer-wall listing)"
merged.loc[merged["creative_id"] == "unknown", "creative_type"] = "unattributed / platform auto"

paid = merged[merged["network"].isin(["Net-A", "Net-B", "Net-C", "Net-D"])].copy()

# All cohorts
summary_all = paid.groupby(["network", "creative_type"]).agg({
    "cost": "sum",
    "impressions_network_reported": "sum",
    "clicks_network_reported": "sum",
    "installs_mmp": "sum"
}).reset_index()

# Mature cohorts (date <= '2025-08-31') for D7 and D30 metrics and retention
mature = paid[paid["date"] <= "2025-08-31"].copy()
summary_mat = mature.groupby(["network", "creative_type"]).agg({
    "cohort_installs": "sum",
    "retained_d1": "sum",
    "retained_d7": "sum",
    "ad_rev_d7_clean": "sum",
    "iap_rev_d7_clean": "sum",
    "ad_rev_d30_clean": "sum",
    "iap_rev_d30_clean": "sum",
    "cost": "sum",
    "installs_mmp": "sum"
}).reset_index()

summary_mat["ret_d1"] = summary_mat["retained_d1"] / summary_mat["cohort_installs"]
summary_mat["ret_d7"] = summary_mat["retained_d7"] / summary_mat["cohort_installs"]
summary_mat["d7_ltv"] = (summary_mat["ad_rev_d7_clean"] + summary_mat["iap_rev_d7_clean"]) / summary_mat["cohort_installs"]
summary_mat["d30_ltv"] = (summary_mat["ad_rev_d30_clean"] + summary_mat["iap_rev_d30_clean"]) / summary_mat["cohort_installs"]
summary_mat["d7_roas"] = (summary_mat["ad_rev_d7_clean"] + summary_mat["iap_rev_d7_clean"]) / summary_mat["cost"]
summary_mat["d30_roas"] = (summary_mat["ad_rev_d30_clean"] + summary_mat["iap_rev_d30_clean"]) / summary_mat["cost"]

perf = summary_all.merge(
    summary_mat[["network", "creative_type", "ret_d1", "ret_d7", "d7_ltv", "d30_ltv", "d7_roas", "d30_roas"]],
    on=["network", "creative_type"],
    how="left"
)

perf["cpm"] = perf["cost"] / (perf["impressions_network_reported"] / 1000.0)
perf["ctr"] = perf["clicks_network_reported"] / perf["impressions_network_reported"]
perf["ipm"] = (perf["installs_mmp"] / perf["impressions_network_reported"]) * 1000.0
perf["cpi"] = perf["cost"] / perf["installs_mmp"]

# Calculate network spend share
net_spends = perf.groupby("network")["cost"].transform("sum")
perf["spend_share"] = perf["cost"] / net_spends

print("\n--- Creative Performance by Type ---")
for _, r in perf.iterrows():
    print(f"{r['network']} | {r['creative_type'][:35]:35s} | Spend: ${r['cost']:>10.2f} ({r['spend_share']*100:>5.1f}%) | Imps: {r['impressions_network_reported']:>10,.0f} | Installs: {r['installs_mmp']:>7,.0f} | CPM: ${r['cpm']:>5.2f} | CTR: {r['ctr']*100:>5.2f}% | IPM: {r['ipm']:>5.2f} | CPI: ${r['cpi']:>5.2f} | D1: {r['ret_d1']*100:>4.1f}% | D7: {r['ret_d7']*100:>4.1f}% | D30 LTV: ${r['d30_ltv']:>5.2f} | D30 ROAS: {r['d30_roas']:>6.3f}")

