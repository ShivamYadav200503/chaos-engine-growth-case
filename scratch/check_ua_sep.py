import csv
from collections import defaultdict

ua_sep = defaultdict(lambda: {"cost": 0.0, "imps": 0, "installs": 0})
with open("data/raw/GameA_ua_daily.csv", "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for r in reader:
        if "2025-09-01" <= r["date"] <= "2025-09-28":
            net = r["network"]
            cost = float(r["cost"])
            imps = int(float(r["impressions_network_reported"]))
            inst = int(float(r["installs_mmp"]))
            ua_sep[net]["cost"] += cost
            ua_sep[net]["imps"] += imps
            ua_sep[net]["installs"] += inst

print("UA Sep 1-28 baseline by network:")
for net, m in sorted(ua_sep.items()):
    if net in ["Net-A", "Net-B", "Net-C", "Net-D"]:
        cpm = (m["cost"] / m["imps"] * 1000) if m["imps"] > 0 else 0
        ipd = (m["imps"] / m["cost"]) if m["cost"] > 0 else 0
        cpi = (m["cost"] / m["installs"]) if m["installs"] > 0 else 0
        print(f"  {net:6s} | Spend: ${m['cost']:>9.2f} | Imps: {m['imps']:>8,d} | CPM: ${cpm:>6.2f} | Imps/$: {ipd:>6.2f} | CPI: ${cpi:>5.2f}")

