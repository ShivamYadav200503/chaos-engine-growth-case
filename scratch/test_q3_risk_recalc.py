import pandas as pd

plan = pd.read_csv("submission/plan.csv")
tot = plan[plan["network"] == "TOTAL"].iloc[0]

tot_spend = float(tot["quarter_spend"])
tot_installs_base = float(tot["expected_installs"])
tot_rev_base = float(tot["expected_d120_revenue"])
tot_roas_base = float(tot["expected_d120_roas"])
cpi_base = tot_spend / tot_installs_base

print(f"Baseline from plan.csv:")
print(f"  Spend:    ${tot_spend:,.2f}")
print(f"  Installs: {tot_installs_base:,.1f} (rounded: {round(tot_installs_base):,})")
print(f"  CPI:      ${cpi_base:.2f}")
print(f"  D120 Rev: ${tot_rev_base:,.2f}")
print(f"  ROAS:     {tot_roas_base*100:.2f}%")

# Scenario 1 (2-Week Delay):
# W1-2 (2/12): 1.0x factor
# W3-4 (2/12): 1.15 / 1.45 factor = 0.793103
# W5-12 (8/12): 1.0x factor
factor_scen1 = (2/12) * 1.0 + (2/12) * (1.15 / 1.45) + (8/12) * 1.0
inst_scen1 = tot_installs_base * factor_scen1
cpi_scen1 = tot_spend / inst_scen1
rev_scen1 = tot_rev_base * factor_scen1
roas_scen1 = rev_scen1 / tot_spend

print(f"\nScenario 1 (2-Week Delay):")
print(f"  Factor:   {factor_scen1:.4f}")
print(f"  Installs: {round(inst_scen1):,} (Lost: {round(tot_installs_base - inst_scen1):,})")
print(f"  CPI:      ${cpi_scen1:.2f} (+{(cpi_scen1/cpi_base - 1)*100:.2f}%)")
print(f"  D120 Rev: ${rev_scen1:,.2f} (Loss: ${tot_rev_base - rev_scen1:,.2f})")
print(f"  ROAS:     {roas_scen1*100:.2f}% (-{(tot_roas_base - roas_scen1)*100:.2f} pts)")

# Scenario 2 (50% Under-Production):
# W1-2 (2/12): 1.0x factor
# W3-12 (10/12): 1.15 / 1.30 factor = 0.884615
factor_scen2 = (2/12) * 1.0 + (10/12) * (1.15 / 1.30)
inst_scen2 = tot_installs_base * factor_scen2
cpi_scen2 = tot_spend / inst_scen2
rev_scen2 = tot_rev_base * factor_scen2
roas_scen2 = rev_scen2 / tot_spend

print(f"\nScenario 2 (50% Under-Production):")
print(f"  Factor:   {factor_scen2:.4f}")
print(f"  Installs: {round(inst_scen2):,} (Lost: {round(tot_installs_base - inst_scen2):,})")
print(f"  CPI:      ${cpi_scen2:.2f} (+{(cpi_scen2/cpi_base - 1)*100:.2f}%)")
print(f"  D120 Rev: ${rev_scen2:,.2f} (Loss: ${tot_rev_base - rev_scen2:,.2f})")
print(f"  ROAS:     {roas_scen2*100:.2f}% (-{(tot_roas_base - roas_scen2)*100:.2f} pts)")

