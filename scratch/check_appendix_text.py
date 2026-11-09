import re

with open("submission/appendix.md", "r", encoding="utf-8") as f:
    text = f.read()

for idx, line in enumerate(text.splitlines(), start=1):
    if "88%" in line or "mix" in line.lower() or "cross-game" in line.lower() or "transfer" in line.lower():
        print(f"Line {idx}: {line[:100]}")

