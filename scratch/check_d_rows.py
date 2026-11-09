import pandas as pd

cr = pd.read_csv("data/processed/GameA_creatives_clean.csv")
d_rows = cr[cr["network"] == "Net-D"]
print(d_rows.groupby("creative_id")[["cost", "impressions_network_reported", "clicks_network_reported", "installs_mmp", "ad_rev_d30_clean", "iap_rev_d30_clean"]].sum())
print("\nSample rows of Net-D:")
print(d_rows[["date", "creative_id", "cost", "impressions_network_reported", "installs_mmp", "iap_rev_d30_clean"]].head(6))
