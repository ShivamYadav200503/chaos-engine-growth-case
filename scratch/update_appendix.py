from pathlib import Path
import re

app_file = Path("submission/appendix.md")
text = app_file.read_text(encoding="utf-8")

# Find the start and end of the bullet points
start_marker = "- **KKT Shadow Price Equilibrations"
end_marker = "- **Organic Uplift Catalyst"

start_idx = text.find(start_marker)
end_idx = text.find(end_marker)
assert start_idx != -1 and end_idx != -1, f"Markers not found: start={start_idx}, end={end_idx}"

new_kkt_section = """- **KKT Shadow Price Equilibrations ($\\lambda \\approx 0.536$):**
  - *Net-A Android Allocation ($68,048 spend; 48.47% budget share):* Core domestic US is paced at 0.90x baseline spend ($31,648.29, delivering post-holiday 0.825x D120 ROAS / 0.960x 1Y ROAS). Top international outperformers (RO, HK, SE, MX, PL, AR, PT, IL, VN, GB) and Regional Tiers 1, 3, 4 are scaled up to 2.0x.
  - *Why Net-D Android US is held at 50.0% ($28,696 spend) while Net-B Android US is at 90.8% ($21,912 spend):* Below 0.50x spend, Net-D captures its maximum allowable scaling efficiency gain ($0.50^{-0.65} = 1.5692\\times$, achieving **1.516x D120 ROAS** after holiday shock and producing **+$14,801 in net D120 cash profit**). However, beyond 0.50x, Net-D's high diminishing returns exponent ($k=0.65$ vs $k=0.40$ on Net-B) drops its marginal D120 revenue to **$0.531 per dollar spent**. This falls strictly below the **$0.536 marginal revenue** where Net-B Android (90.8%), Net-B iOS (67.4%), and Net-C Android (60.7%) equilibrate under KKT optimality conditions. Capital allocated beyond 0.50x on Net-D produces less revenue than deploying it on Net-B and Net-C.
  - *Active Lines Post-Holiday Effective ROAS:* Net-B Android US achieves post-holiday effective **0.893x D120 ROAS / 0.960x 1Y ROAS** ($21,911.56 spend; 0.982x mature); Net-B iOS US achieves **0.893x D120 ROAS / 0.950x 1Y ROAS** ($13,725.49 spend; 0.979x mature); Net-C Android US achieves **0.975x D120 ROAS / 1.076x 1Y ROAS** ($8,011.14 spend; 1.244x mature).
  - *Counter-Intuitive Budget Allocation (The "Cheap-CPI Trap"):* Portfolio optimization allocates capital to maximize net margin ($\\text{LTV} - \\text{CPI}$), not minimize gross CPI. Consequently, higher-CPI cells like `Net-A GB` ($1.84 CPI) and `SE` ($0.79 CPI) receive maximum **2.0x budget multiples** because their strong monetization delivers >1.00x D120 payback. In contrast, superficial "cheap-CPI" traps like `IT` ($0.20 CPI), `PH` ($0.30 CPI), `SA` ($0.58 CPI), `SK`, and `AT` are held at the 0.50x–0.60x retention floor ($68–$192 per geo) because their weak player monetization fails to return capital (e.g., SA D120 ROAS is only 0.632x; AT is 0.585x).
"""

text = text[:start_idx] + new_kkt_section + text[end_idx:]

# Replace all file:/// links
text = re.sub(r'file:///[cC]:/[^)]*?/submission/', './', text)
text = re.sub(r'file:///[cC]:/[^)]*?/outputs/', '../outputs/', text)

app_file.write_text(text, encoding="utf-8")
print("Successfully synchronized submission/appendix.md!")
