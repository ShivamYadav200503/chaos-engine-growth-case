from pathlib import Path
import re
import pandas as pd

def count_pages(pdf_path):
    with open(pdf_path, 'rb') as f:
        data = f.read()
    return len(re.findall(rb'/Type\s*/Page\b', data))

print('=== PROGRAMMATIC PAGE COUNT AUDIT ===')
for name, max_p in [('submission/memo.pdf', 2), ('submission/ai_log/ai_usage_log.pdf', 1), ('submission/appendix.pdf', 12)]:
    p = count_pages(name)
    print(f'{name}: {p} pages (Limit: <= {max_p}) -> PASS: {p <= max_p}')

print('\n=== PLAN.CSV TOTAL ROW VS MEMO.MD RECONCILIATION ===')
df = pd.read_csv('submission/plan.csv')
tot = df[df['network'] == 'TOTAL'].iloc[0]
print(f"plan.csv quarter_spend:       ${tot['quarter_spend']:,.2f}")
print(f"plan.csv expected_installs:   {tot['expected_installs']:,.1f} paid installs")
print(f"plan.csv expected_d120_rev:   ${tot['expected_d120_revenue']:,.2f}")
print(f"plan.csv expected_d120_roas:  {tot['expected_d120_roas']:.4f}x")
print(f"plan.csv expected_1y_revenue: ${tot['expected_1y_revenue']:,.2f}")
print(f"plan.csv expected_1y_roas:    {tot['expected_1y_roas']:.4f}x")

with open('submission/memo.md', 'r', encoding='utf-8') as f:
    memo_text = f.read()

line2 = [line for line in memo_text.splitlines() if line.startswith('2. **Expected Result:')][0]
print('\nmemo.md Line 2 (Expected Result):')
print(line2)

