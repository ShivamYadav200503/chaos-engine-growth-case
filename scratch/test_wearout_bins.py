import csv
from collections import defaultdict

# Track each creative's daily progression sorted by date
# Read all daily rows for Game A paid creatives
rows = []
with open("data/processed/GameA_creatives_clean.csv", "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for r in reader:
        net = r["network"]
        if net not in ["Net-A", "Net-B", "Net-C", "Net-D"]:
            continue
        c_id = r["creative_id"]
        if net == "Net-D" and c_id == "unknown":
            c_id = "A-K029"
        if c_id == "unknown":
            continue
            
        rows.append({
            "network": net,
            "creative_id": c_id,
            "date": r["date"],
            "cost": float(r["cost"]),
            "impressions": int(float(r["impressions_network_reported"])),
            "installs": int(float(r["installs_mmp"]))
        })

# Sort by date
rows.sort(key=lambda x: x["date"])

# Group by (network, creative_id) and compute running cumulative impressions
# Then assign each record to a cumulative impression bucket:
# 0 - 100k, 100k - 500k, 500k - 1.5M, > 1.5M
bins = [
    ("0 to 100k", 0, 100_000),
    ("100k to 500k", 100_000, 500_000),
    ("500k to 1.5M", 500_000, 1_500_000),
    ("> 1.5M", 1_500_000, float("inf"))
]

bucket_agg = defaultdict(lambda: {
    "cost": 0.0,
    "impressions": 0,
    "installs": 0
})

cum_imps = defaultdict(int)

for r in rows:
    key = (r["network"], r["creative_id"])
    prev_cum = cum_imps[key]
    new_cum = prev_cum + r["impressions"]
    cum_imps[key] = new_cum
    
    # Midpoint of cumulative imps for this day
    mid_cum = (prev_cum + new_cum) / 2.0
    
    # Find bin
    b_label = "> 1.5M"
    for label, low, high in bins:
        if low <= mid_cum < high:
            b_label = label
            break
            
    b_key = (r["network"], b_label)
    bucket_agg[b_key]["cost"] += r["cost"]
    bucket_agg[b_key]["impressions"] += r["impressions"]
    bucket_agg[b_key]["installs"] += r["installs"]

print("--- Empirical Wear-out by Cumulative Impression Tier ---")
for net in ["Net-A", "Net-B", "Net-C", "Net-D"]:
    print(f"\n{net}:")
    for label, _, _ in bins:
        b_key = (net, label)
        if b_key in bucket_agg:
            m = bucket_agg[b_key]
            cpi = (m["cost"] / m["installs"]) if m["installs"] > 0 else 0
            ipm = (m["installs"] / m["impressions"] * 1000) if m["impressions"] > 0 else 0
            cpm = (m["cost"] / m["impressions"] * 1000) if m["impressions"] > 0 else 0
            print(f"  {label:15s} | Imps: {m['impressions']:>9,d} | Inst: {m['installs']:>6,d} | CPM: ${cpm:>5.2f} | IPM: {ipm:>5.2f} | CPI: ${cpi:>5.2f}")

