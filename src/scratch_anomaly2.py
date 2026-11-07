"""Anomaly deep-dive part 2: revenue censoring, Net-A GameB overcount, ad_rev vs all_sources."""
import pandas as pd
import numpy as np

raw = r"c:\Users\sy422\OneDrive\Documents\GitHub\chaos-engine-growth-case\data\raw"

### BUG 1: Right-censoring not implemented — ad_rev_d120/d180 filled for 2-day-old cohorts
# These are NOT real values. The data has zeros where cohort has 0 installs, and
# copies of shorter-horizon values for recent cohorts.
print("=" * 80)
print("BUG 1: Revenue right-censoring pattern")
print("=" * 80)
for game in ["GameA", "GameB"]:
    df = pd.read_csv(f"{raw}/{game}_cohorts.csv", low_memory=False)
    df["install_date"] = pd.to_datetime(df["install_date"])
    df["age"] = (pd.Timestamp("2025-09-30") - df["install_date"]).dt.days
    
    # Show the pattern: for young cohorts, are d30/d60/d90/d120 all equal?
    young = df[(df["age"] >= 7) & (df["age"] < 30) & (df["ad_rev_d7"] > 0)].head(20)
    print(f"\n{game} - cohorts aged 7-29d, checking if d7==d14==d30==d60==d90==d120==d180:")
    cols = ["ad_rev_d7", "ad_rev_d14", "ad_rev_d30", "ad_rev_d60", "ad_rev_d90", "ad_rev_d120", "ad_rev_d180"]
    for _, row in young.iterrows():
        vals = [row[c] for c in cols]
        print(f"  age={row['age']:3d}d  d7={vals[0]:.4f}  d14={vals[1]:.4f}  d30={vals[2]:.4f}  d60={vals[3]:.4f}  d120={vals[5]:.4f}  d180={vals[6]:.4f}  all_same={len(set(vals))==1}")

### BUG 2: GameB Net-A installs_network_reported wildly overcounted
print("\n" + "=" * 80)
print("BUG 2: GameB Net-A network-reported installs anomaly")
print("=" * 80)
df = pd.read_csv(f"{raw}/GameB_ua_daily.csv", low_memory=False)
neta = df[df["network"] == "Net-A"]
neta["date"] = pd.to_datetime(neta["date"])
monthly = neta.groupby(neta["date"].dt.to_period("M")).agg(
    mmp=("installs_mmp", "sum"),
    net=("installs_network_reported", "sum"),
    cost=("cost", "sum"),
).reset_index()
monthly["ratio"] = monthly["mmp"] / monthly["net"]
print(monthly.to_string(index=False))

### BUG 3: ad_rev_all_sources is ~2x ad_rev — which to use?
print("\n" + "=" * 80)
print("BUG 3: ad_rev vs ad_rev_all_sources (mediation vs all)")
print("=" * 80)
for game in ["GameA", "GameB"]:
    df = pd.read_csv(f"{raw}/{game}_cohorts.csv", low_memory=False)
    df["install_date"] = pd.to_datetime(df["install_date"])
    df["age"] = (pd.Timestamp("2025-09-30") - df["install_date"]).dt.days
    mature = df[df["age"] >= 30]
    
    # Per-network comparison
    for net in sorted(mature["network"].unique()):
        sub = mature[mature["network"] == net]
        ad7 = sub["ad_rev_d7"].sum()
        all7 = sub["ad_rev_all_sources_d7"].sum()
        if ad7 > 0:
            ratio = all7 / ad7
            print(f"{game} {net:15s}: ad_rev_d7=${ad7:10,.0f}  all_sources_d7=${all7:10,.0f}  ratio={ratio:.3f}")

### BUG 4: ad_rev_d180 < ad_rev_d120 (non-monotonicity)
print("\n" + "=" * 80)
print("BUG 4: ad_rev_d180 < ad_rev_d120 non-monotonicity")
print("=" * 80)
for game in ["GameA", "GameB"]:
    df = pd.read_csv(f"{raw}/{game}_cohorts.csv", low_memory=False)
    df["install_date"] = pd.to_datetime(df["install_date"])
    df["age"] = (pd.Timestamp("2025-09-30") - df["install_date"]).dt.days
    
    # Only check truly mature cohorts (age >= 180)
    mature180 = df[df["age"] >= 180]
    bad = mature180[mature180["ad_rev_d180"] < mature180["ad_rev_d120"]]
    print(f"{game}: {len(bad)} of {len(mature180)} fully mature cohorts have d180 < d120")
    if len(bad) > 0:
        bad["diff"] = bad["ad_rev_d120"] - bad["ad_rev_d180"]
        print(f"  Mean shortfall: ${bad['diff'].mean():.4f} per cohort")
        print(f"  Networks: {bad['network'].value_counts().to_dict()}")

### BUG 5: 'unknown' platform with 0 installs
print("\n" + "=" * 80)
print("BUG 5: unknown platform rows")
print("=" * 80)
for game in ["GameA", "GameB"]:
    df = pd.read_csv(f"{raw}/{game}_cohorts.csv", low_memory=False)
    unk = df[df["platform"] == "unknown"]
    print(f"{game} 'unknown' platform: {len(unk)} rows, total installs={unk['installs'].sum()}, total ad_rev_d7={unk['ad_rev_d7'].sum():.2f}")

### BUG 6: Telemetry starts late for GameA (March 27 vs Jan 6)
print("\n" + "=" * 80)
print("BUG 6: GameA telemetry missing first ~80 days")
print("=" * 80)
t_a = pd.read_csv(f"{raw}/GameA_telemetry_daily.csv", low_memory=False)
t_b = pd.read_csv(f"{raw}/GameB_telemetry_daily.csv", low_memory=False)
print(f"GameA telemetry: {t_a['date'].min()} to {t_a['date'].max()} ({len(t_a)} rows)")
print(f"GameB telemetry: {t_b['date'].min()} to {t_b['date'].max()} ({len(t_b)} rows)")

### BUG 7: Null countries in telemetry
print("\n" + "=" * 80)
print("BUG 7: Null countries in telemetry")
print("=" * 80)
for game in ["GameA", "GameB"]:
    t = pd.read_csv(f"{raw}/{game}_telemetry_daily.csv", low_memory=False)
    null_c = t[t["country"].isna()]
    print(f"{game}: {len(null_c)} rows with null country, DAU sum={null_c['dau'].sum()}")

### Revenue per install sanity check by network
print("\n" + "=" * 80)
print("Revenue per install by network (mature cohorts)")
print("=" * 80)
for game in ["GameA", "GameB"]:
    df = pd.read_csv(f"{raw}/{game}_cohorts.csv", low_memory=False)
    df["install_date"] = pd.to_datetime(df["install_date"])
    df["age"] = (pd.Timestamp("2025-09-30") - df["install_date"]).dt.days
    mature = df[df["age"] >= 120]
    
    for net in sorted(mature["network"].unique()):
        sub = mature[mature["network"] == net]
        inst = sub["installs"].sum()
        if inst > 0:
            ad120 = sub["ad_rev_d120"].sum() / inst
            iap120 = sub["iap_rev_d120"].sum() / inst
            total120 = ad120 + iap120
            print(f"{game} {net:15s}: installs={inst:7d}  ad_rev/inst=${ad120:.4f}  iap_rev/inst=${iap120:.4f}  total=${total120:.4f}")

