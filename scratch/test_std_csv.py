import csv

cols = None
rows = []
with open("data/processed/GameA_creatives_clean.csv", "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    cols = next(reader)
    count = 0
    for r in reader:
        count += 1

print("Successfully read with standard csv! Total rows:", count)
print("Columns:", cols)

