import os
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["OMP_NUM_THREADS"] = "1"

import pandas as pd
from pathlib import Path

df = pd.read_csv('data/processed/GameA_creatives_clean.csv', nrows=5)
print('GameA_creatives_clean columns:', list(df.columns))

cat = pd.read_csv('data/raw/GameA_creatives_catalog.csv')
print('\nGameA_creatives_catalog:')
print(cat.to_string())
