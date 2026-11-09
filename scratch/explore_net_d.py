import pandas as pd

cr = pd.read_csv("data/processed/GameA_creatives_clean.csv")
cat = pd.read_csv("data/raw/GameA_creatives_catalog.csv")

print("=== Net-D rows in cr ===")
d_rows = cr[cr["network"] == "Net-D"]
print(d_rows[["date", "network", "creative_id", "cost", "installs_mmp", "impressions_network_reported"]].head(10))
print("Net-D total cost:", d_rows["cost"].sum())
print("Net-D total installs:", d_rows["installs_mmp"].sum())
print("Net-D total impressions:", d_rows["impressions_network_reported"].sum())
print("Net-D creative_ids in cr:", d_rows["creative_id"].value_counts(dropna=False))

print("\n=== All networks cost & impressions in cr ===")
print(cr.groupby("network")[["cost", "impressions_network_reported", "installs_mmp"]].sum())

print("\n=== Compare cr with ua for Net-D ===")
ua = pd.read_csv("data/raw/GameA_ua_daily.csv")
print(ua.groupby("network")[["cost", "impressions_network_reported", "installs_mmp"]].sum())
