import csv
from collections import defaultdict

# Spend by network in CFO plan
spend_by_net = {
    "Net-A": 68051.05,
    "Net-B": 35634.41,
    "Net-C": 8010.59,
    "Net-D": 28695.54,
}
total_spend = sum(spend_by_net.values())

# Base CPI from Sep baseline
base_cpi = {
    "Net-A": 1.13,
    "Net-B": 5.89,
    "Net-C": 2.41,
    "Net-D": 8.06,
}

# Base installs at base CPI (before wearout)
base_installs = {net: spend_by_net[net] / base_cpi[net] for net in spend_by_net}
tot_base_installs = sum(base_installs.values())

# BASELINE (On-Time, 13 units):
# W1-W2: existing creatives, avg wearout ~+7.5% to +15%
# W3-W12: new creatives refreshed at 100% cap (max +30%, avg +15%)
# Lifecycle average CPI inflation = +15.0%
cpi_baseline = {net: base_cpi[net] * 1.15 for net in spend_by_net}
installs_baseline = {net: spend_by_net[net] / cpi_baseline[net] for net in spend_by_net}
tot_installs_baseline = sum(installs_baseline.values())
portfolio_cpi_baseline = total_spend / tot_installs_baseline

# SCENARIO 1 (2-Week Delay: New creatives arrive Week 5):
# W1-W2: existing carry (avg +15%)
# W3-W4: existing creatives forced to run extra 2 weeks -> terminal wear reaches +60%, avg wear in W3-W4 is +45% (factor 1.45)
# W5-W12: new creatives arrive, run with normal +15% avg wear
# For W3-W4 (2/12 of spend): CPI inflation is 1.45 instead of 1.15
# Effective quarter multiplier = (2/12 * 1.15) + (2/12 * 1.45) + (8/12 * 1.15) = 1.20 (avg +20% instead of +15%)
installs_scen1 = {}
for net in spend_by_net:
    w1_2_spend = spend_by_net[net] * (2/12)
    w3_4_spend = spend_by_net[net] * (2/12)
    w5_12_spend = spend_by_net[net] * (8/12)
    
    inst_1_2 = w1_2_spend / (base_cpi[net] * 1.15)
    inst_3_4 = w3_4_spend / (base_cpi[net] * 1.45)
    inst_5_12 = w5_12_spend / (base_cpi[net] * 1.15)
    installs_scen1[net] = inst_1_2 + inst_3_4 + inst_5_12

tot_installs_scen1 = sum(installs_scen1.values())
portfolio_cpi_scen1 = total_spend / tot_installs_scen1

# SCENARIO 2 (50% Under-Production: Only 6-7 units built):
# Creatives run 2x their lifespan -> wear reaches +60% terminal, average lifecycle CPI inflation is +30.0% (factor 1.30)
# W1-W2 (2/12): existing carry (1.15)
# W3-W12 (10/12): underproduced new creatives (1.30)
installs_scen2 = {}
for net in spend_by_net:
    w1_2_spend = spend_by_net[net] * (2/12)
    w3_12_spend = spend_by_net[net] * (10/12)
    
    inst_1_2 = w1_2_spend / (base_cpi[net] * 1.15)
    inst_3_12 = w3_12_spend / (base_cpi[net] * 1.30)
    installs_scen2[net] = inst_1_2 + inst_3_12

tot_installs_scen2 = sum(installs_scen2.values())
portfolio_cpi_scen2 = total_spend / tot_installs_scen2

# D120 LTV per install (portfolio weighted):
# In Q2, D120 revenue in CFO plan was ~$140,896 on ~73k installs (~$1.93 per install)
d120_ltv_per_install = 140896.0 / tot_installs_baseline

rev_baseline = tot_installs_baseline * d120_ltv_per_install
rev_scen1 = tot_installs_scen1 * d120_ltv_per_install
rev_scen2 = tot_installs_scen2 * d120_ltv_per_install

roas_baseline = rev_baseline / total_spend
roas_scen1 = rev_scen1 / total_spend
roas_scen2 = rev_scen2 / total_spend

print(f"--- Q3 FATIGUE RISK SIMULATION ---")
print(f"Baseline (13 Units, On-Time):")
print(f"  Installs: {tot_installs_baseline:,.0f} | Portfolio CPI: ${portfolio_cpi_baseline:.2f} | D120 Rev: ${rev_baseline:,.2f} | D120 ROAS: {roas_baseline*100:.2f}%")
print(f"\nScenario 1 (2-Week Delay in Batch 1):")
print(f"  Installs: {tot_installs_scen1:,.0f} (Lost: {tot_installs_baseline - tot_installs_scen1:,.0f}) | Portfolio CPI: ${portfolio_cpi_scen1:.2f} (+{(portfolio_cpi_scen1/portfolio_cpi_baseline - 1)*100:.2f}%)")
print(f"  D120 Rev: ${rev_scen1:,.2f} (Loss: ${rev_baseline - rev_scen1:,.2f}) | D120 ROAS: {roas_scen1*100:.2f}% (-{(roas_baseline - roas_scen1)*100:.2f} pts)")
print(f"\nScenario 2 (50% Under-Production, 6-7 Units):")
print(f"  Installs: {tot_installs_scen2:,.0f} (Lost: {tot_installs_baseline - tot_installs_scen2:,.0f}) | Portfolio CPI: ${portfolio_cpi_scen2:.2f} (+{(portfolio_cpi_scen2/portfolio_cpi_baseline - 1)*100:.2f}%)")
print(f"  D120 Rev: ${rev_scen2:,.2f} (Loss: ${rev_baseline - rev_scen2:,.2f}) | D120 ROAS: {roas_scen2*100:.2f}% (-{(roas_baseline - roas_scen2)*100:.2f} pts)")

