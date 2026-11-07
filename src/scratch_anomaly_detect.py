"""Quick deep anomaly detection across all raw files."""
import pandas as pd
import numpy as np

raw = r"c:\Users\sy422\OneDrive\Documents\GitHub\chaos-engine-growth-case\data\raw"

print("=" * 80)
print("ANOMALY DETECTION DEEP DIVE")
print("=" * 80)

### 1. Right-censoring check in cohorts
for game in ["GameA", "GameB"]:
    df = pd.read_csv(f"{raw}/{game}_cohorts.csv", low_memory=False)
    df["install_date"] = pd.to_datetime(df["install_date"])
    as_of = pd.Timestamp("2025-09-30")
    df["age_days"] = (as_of - df["install_date"]).dt.days

    # Cohorts < 120 days old shouldn't have d120 data
    young_d120 = df[(df["age_days"] < 120) & (df["ad_rev_d120"] > 0)]
    print(f"{game}: cohorts < 120d old with ad_rev_d120 > 0: {len(young_d120)}")

    young_d180 = df[(df["age_days"] < 180) & (df["ad_rev_d180"] > 0)]
    print(f"{game}: cohorts < 180d old with ad_rev_d180 > 0: {len(young_d180)}")

    young_ret120 = df[(df["age_days"] < 120) & (df["retained_d120"] > 0)]
    print(f"{game}: cohorts < 120d old with retained_d120 > 0: {len(young_ret120)}")

    # Check 0 vs NaN pattern
    recent = df[df["age_days"] < 30]
    d120_col = "ad_rev_d120"
    d60_col = "ad_rev_d60"
    print(f"  recent (<30d): d120 nulls={recent[d120_col].isna().sum()}, zeros={(recent[d120_col]==0).sum()}, pos={(recent[d120_col]>0).sum()}")
    print(f"  recent (<30d): d60 nulls={recent[d60_col].isna().sum()}, zeros={(recent[d60_col]==0).sum()}, pos={(recent[d60_col]>0).sum()}")
    
    # Check maturity cutoffs: what's the earliest cohort age that has non-zero d120?
    has_d120 = df[df["ad_rev_d120"] > 0]
    if len(has_d120) > 0:
        print(f"  Earliest cohort age with d120>0: {has_d120['age_days'].min()} days")
    has_d180 = df[df["ad_rev_d180"] > 0]
    if len(has_d180) > 0:
        print(f"  Earliest cohort age with d180>0: {has_d180['age_days'].min()} days")
    print()

### 2. MMP vs Network install discrepancy
for game in ["GameA", "GameB"]:
    df = pd.read_csv(f"{raw}/{game}_ua_daily.csv", low_memory=False)
    paid_nets = ["Net-A", "Net-B", "Net-C", "Net-D", "Net-E", "Net-F"]
    paid = df[df["network"].isin(paid_nets)]
    total_mmp = paid["installs_mmp"].sum()
    total_net = paid["installs_network_reported"].sum()
    ratio = total_mmp / total_net if total_net > 0 else 0
    print(f"{game} paid: MMP/Network ratio = {ratio:.3f} (MMP={total_mmp}, Net={total_net})")

    for net in sorted(paid["network"].unique()):
        sub = paid[paid["network"] == net]
        net_rep = sub["installs_network_reported"].sum()
        mmp_rep = sub["installs_mmp"].sum()
        r = mmp_rep / net_rep if net_rep > 0 else 0
        cost = sub["cost"].sum()
        print(f"  {net}: ratio={r:.3f}  MMP={mmp_rep}  Net={net_rep}  Cost=${cost:,.0f}")
    print()

### 3. Platform anomalies
for game in ["GameA", "GameB"]:
    df = pd.read_csv(f"{raw}/{game}_ua_daily.csv", low_memory=False)
    for p in ["android-tv", "windows", "unknown"]:
        sub = df[df["platform"] == p]
        if len(sub) > 0:
            print(f"{game} ua_daily platform={p}: {len(sub)} rows, installs_mmp={sub['installs_mmp'].sum()}, cost=${sub['cost'].sum():,.0f}")
    cohorts = pd.read_csv(f"{raw}/{game}_cohorts.csv", low_memory=False)
    for p in ["android-tv", "windows", "unknown"]:
        sub = cohorts[cohorts["platform"] == p]
        if len(sub) > 0:
            print(f"{game} cohorts platform={p}: {len(sub)} rows, installs={sub['installs'].sum()}")
    print()

### 4. Invalid Signature campaigns
for game in ["GameA", "GameB"]:
    df = pd.read_csv(f"{raw}/{game}_ua_daily.csv", low_memory=False)
    inv = df[df["campaign_id"] == "Invalid Signature"]
    if len(inv) > 0:
        print(f"{game} Invalid Signature: {len(inv)} rows, installs_mmp={inv['installs_mmp'].sum()}, networks={inv['network'].unique()}")
    print()

### 5. ad_rev vs ad_rev_all_sources comparison
for game in ["GameA", "GameB"]:
    df = pd.read_csv(f"{raw}/{game}_cohorts.csv", low_memory=False)
    df["install_date"] = pd.to_datetime(df["install_date"])
    as_of = pd.Timestamp("2025-09-30")
    df["age_days"] = (as_of - df["install_date"]).dt.days
    
    mature = df[df["age_days"] >= 30]
    ad_d0 = mature["ad_rev_d0"].sum()
    ad_all_d0 = mature["ad_rev_all_sources_d0"].sum()
    print(f"{game} mature cohorts: ad_rev_d0 total=${ad_d0:,.0f}, ad_rev_all_sources_d0 total=${ad_all_d0:,.0f}, ratio={ad_all_d0/ad_d0:.3f}" if ad_d0 > 0 else f"{game}: ad_rev_d0=0")
    
    ad_d7 = mature["ad_rev_d7"].sum()
    ad_all_d7 = mature["ad_rev_all_sources_d7"].sum()
    print(f"  ad_rev_d7=${ad_d7:,.0f}, ad_rev_all_sources_d7=${ad_all_d7:,.0f}, ratio={ad_all_d7/ad_d7:.3f}" if ad_d7 > 0 else "  ad_rev_d7=0")
    
    ad_d30 = mature["ad_rev_d30"].sum()
    ad_all_d30 = mature["ad_rev_all_sources_d30"].sum()
    print(f"  ad_rev_d30=${ad_d30:,.0f}, ad_rev_all_sources_d30=${ad_all_d30:,.0f}, ratio={ad_all_d30/ad_d30:.3f}" if ad_d30 > 0 else "  ad_rev_d30=0")
    print()

### 6. Telemetry date range vs UA date range
for game in ["GameA", "GameB"]:
    ua = pd.read_csv(f"{raw}/{game}_ua_daily.csv", low_memory=False)
    telem = pd.read_csv(f"{raw}/{game}_telemetry_daily.csv", low_memory=False)
    print(f"{game} UA date range: {ua['date'].min()} to {ua['date'].max()}")
    print(f"{game} Telemetry date range: {telem['date'].min()} to {telem['date'].max()}")
    print()

### 7. Country 'zz' in GameB
for game in ["GameA", "GameB"]:
    df = pd.read_csv(f"{raw}/{game}_cohorts.csv", low_memory=False)
    zz = df[df["country"] == "zz"]
    if len(zz) > 0:
        print(f"{game} country='zz': {len(zz)} rows, installs={zz['installs'].sum()}, networks={zz['network'].unique()}")
    blank = df[df["country"].isna() | (df["country"] == "")]
    if len(blank) > 0:
        print(f"{game} blank country: {len(blank)} rows")
    print()

### 8. Retained > Installs check
for game in ["GameA", "GameB"]:
    df = pd.read_csv(f"{raw}/{game}_cohorts.csv", low_memory=False)
    bad_ret = df[df["retained_d1"] > df["installs"]]
    if len(bad_ret) > 0:
        print(f"{game}: retained_d1 > installs in {len(bad_ret)} rows")
    for col in ["retained_d3", "retained_d7", "retained_d14", "retained_d30"]:
        bad = df[df[col] > df["installs"]]
        if len(bad) > 0:
            print(f"{game}: {col} > installs in {len(bad)} rows")
    print()

### 9. Cost but 0 installs (or vice versa)
for game in ["GameA", "GameB"]:
    df = pd.read_csv(f"{raw}/{game}_ua_daily.csv", low_memory=False)
    paid = df[df["network"].isin(["Net-A", "Net-B", "Net-C", "Net-D", "Net-E", "Net-F"])]
    cost_no_inst = paid[(paid["cost"] > 0) & (paid["installs_mmp"] == 0)]
    inst_no_cost = paid[(paid["installs_mmp"] > 0) & (paid["cost"] == 0)]
    print(f"{game}: cost>0 but 0 MMP installs: {len(cost_no_inst)} rows, total cost=${cost_no_inst['cost'].sum():,.0f}")
    print(f"{game}: MMP installs>0 but 0 cost: {len(inst_no_cost)} rows, total installs={inst_no_cost['installs_mmp'].sum()}")
    print()

### 10. Monotonicity check on cumulative revenue columns
for game in ["GameA", "GameB"]:
    df = pd.read_csv(f"{raw}/{game}_cohorts.csv", low_memory=False)
    df["install_date"] = pd.to_datetime(df["install_date"])
    as_of = pd.Timestamp("2025-09-30")
    df["age_days"] = (as_of - df["install_date"]).dt.days
    
    ad_cols = ["ad_rev_d0", "ad_rev_d1", "ad_rev_d3", "ad_rev_d7", "ad_rev_d14", "ad_rev_d30", "ad_rev_d60", "ad_rev_d90", "ad_rev_d120", "ad_rev_d180"]
    ad_days = [0, 1, 3, 7, 14, 30, 60, 90, 120, 180]
    
    violations = 0
    for i in range(len(ad_cols) - 1):
        c1, c2 = ad_cols[i], ad_cols[i+1]
        d1, d2 = ad_days[i], ad_days[i+1]
        # Only check if cohort is old enough for the later day
        mask = df["age_days"] >= d2
        bad = df[mask & (df[c2] < df[c1]) & (df[c2] > 0)]
        if len(bad) > 0:
            violations += len(bad)
            print(f"{game}: {c2} < {c1} in {len(bad)} mature rows")
    
    if violations == 0:
        print(f"{game}: ad_rev monotonicity OK for mature cohorts")
    
    # Same for IAP
    iap_cols = ["iap_rev_d0", "iap_rev_d1", "iap_rev_d3", "iap_rev_d7", "iap_rev_d14", "iap_rev_d30", "iap_rev_d60", "iap_rev_d90", "iap_rev_d120", "iap_rev_d180"]
    violations = 0
    for i in range(len(iap_cols) - 1):
        c1, c2 = iap_cols[i], iap_cols[i+1]
        d1, d2 = ad_days[i], ad_days[i+1]
        mask = df["age_days"] >= d2
        bad = df[mask & (df[c2] < df[c1]) & (df[c2] > 0)]
        if len(bad) > 0:
            violations += len(bad)
            print(f"{game}: {c2} < {c1} in {len(bad)} mature rows")
    if violations == 0:
        print(f"{game}: iap_rev monotonicity OK for mature cohorts")
    print()

