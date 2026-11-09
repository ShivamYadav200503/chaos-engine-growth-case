import csv
from collections import defaultdict

# 1. Load catalog
catalog = {}
with open("data/raw/GameA_creatives_catalog.csv", "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        catalog[(row["network"], row["creative_id"])] = row["creative_type"]

# 2. Aggregators
# Key: (network, creative_id)
# Metrics: cost, imps, clicks, installs, mature_installs, ret_d1, ret_d7, d7_rev, d30_rev
agg = defaultdict(lambda: {
    "cost": 0.0,
    "impressions": 0,
    "clicks": 0,
    "installs": 0,
    "mature_installs": 0,
    "ret_d1": 0,
    "ret_d7": 0,
    "mature_cost": 0.0,
    "d7_rev": 0.0,
    "d30_rev": 0.0
})

with open("data/processed/GameA_creatives_clean.csv", "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for r in reader:
        net = r["network"]
        if net not in ["Net-A", "Net-B", "Net-C", "Net-D"]:
            continue
            
        c_id = r["creative_id"]
        # Handle Net-D attribution:
        if net == "Net-D" and c_id == "unknown":
            c_id = "A-K029"
            
        cost = float(r["cost"])
        imps = int(float(r["impressions_network_reported"]))
        clicks = int(float(r["clicks_network_reported"]))
        installs = int(float(r["installs_mmp"]))
        date = r["date"]
        
        # Accumulate all
        entry = agg[(net, c_id)]
        entry["cost"] += cost
        entry["impressions"] += imps
        entry["clicks"] += clicks
        entry["installs"] += installs
        
        # Mature cohorts (date <= 2025-08-31)
        if date <= "2025-08-31":
            cohort_inst = int(float(r["cohort_installs"]))
            ret1 = int(float(r["retained_d1"]))
            ret7 = int(float(r["retained_d7"]))
            ad7 = float(r["ad_rev_d7_clean"])
            iap7 = float(r["iap_rev_d7_clean"])
            ad30 = float(r["ad_rev_d30_clean"])
            iap30 = float(r["iap_rev_d30_clean"])
            
            entry["mature_cost"] += cost
            entry["mature_installs"] += cohort_inst
            entry["ret_d1"] += ret1
            entry["ret_d7"] += ret7
            entry["d7_rev"] += (ad7 + iap7)
            entry["d30_rev"] += (ad30 + iap30)

print(f"Aggregated {len(agg)} (network, creative_id) pairs!")

# Now aggregate by (network, creative_type)
type_agg = defaultdict(lambda: {
    "cost": 0.0,
    "impressions": 0,
    "clicks": 0,
    "installs": 0,
    "mature_cost": 0.0,
    "mature_installs": 0,
    "ret_d1": 0,
    "ret_d7": 0,
    "d7_rev": 0.0,
    "d30_rev": 0.0
})

for (net, c_id), m in agg.items():
    ctype = catalog.get((net, c_id), "unattributed / platform auto")
    if c_id == "A-K029":
        ctype = "store image (offer-wall listing)"
    t_entry = type_agg[(net, ctype)]
    for k, v in m.items():
        t_entry[k] += v

print("\n--- Network & Creative Type Summary ---")
# Network spend totals for share
net_spend_tot = defaultdict(float)
for (net, _), m in type_agg.items():
    net_spend_tot[net] += m["cost"]

for (net, ctype), m in sorted(type_agg.items()):
    cpm = (m["cost"] / m["impressions"] * 1000) if m["impressions"] > 0 else 0
    ctr = (m["clicks"] / m["impressions"] * 100) if m["impressions"] > 0 else 0
    ipm = (m["installs"] / m["impressions"] * 1000) if m["impressions"] > 0 else 0
    cpi = (m["cost"] / m["installs"]) if m["installs"] > 0 else 0
    share = (m["cost"] / net_spend_tot[net] * 100) if net_spend_tot[net] > 0 else 0
    
    ret1_pct = (m["ret_d1"] / m["mature_installs"] * 100) if m["mature_installs"] > 0 else 0
    ret7_pct = (m["ret_d7"] / m["mature_installs"] * 100) if m["mature_installs"] > 0 else 0
    d7_ltv = (m["d7_rev"] / m["mature_installs"]) if m["mature_installs"] > 0 else 0
    d30_ltv = (m["d30_rev"] / m["mature_installs"]) if m["mature_installs"] > 0 else 0
    d30_roas = (m["d30_rev"] / m["mature_cost"]) if m["mature_cost"] > 0 else 0
    
    print(f"{net:5s} | {ctype[:35]:35s} | Spend: ${m['cost']:>10.2f} ({share:>5.1f}%) | Imps: {m['impressions']:>10,d} | Inst: {m['installs']:>7,d} | CPM: ${cpm:>5.2f} | CTR: {ctr:>5.2f}% | IPM: {ipm:>5.2f} | CPI: ${cpi:>5.2f} | D1: {ret1_pct:>4.1f}% | D7: {ret7_pct:>4.1f}% | D30 LTV: ${d30_ltv:>5.2f} | D30 ROAS: {d30_roas:>6.3f}")

