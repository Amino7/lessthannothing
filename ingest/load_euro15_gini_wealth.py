"""
load_euro15.py
--------------
Loads euro15.csv from the gut-leben-in-deutschland GitHub repo
and saves it to data/raw/

Run from project root:
    python scripts/load_euro15.py
"""

import os
import requests
import pandas as pd


RAW_DIR = os.path.join("data", "raw")
CLEAN_DIR = os.path.join("data", "clean")
os.makedirs(RAW_DIR, exist_ok=True)
os.makedirs(CLEAN_DIR, exist_ok=True)


url = "https://raw.githubusercontent.com/gut-leben-in-deutschland/bericht/master/content/05/03/euro15.csv"

print("Fetching euro15.csv...")
response = requests.get(url, timeout=30)
print(f"  Status: {response.status_code}")

raw_path = os.path.join(RAW_DIR, "euro15_gini_wealth.csv")
with open(raw_path, "w", encoding="utf-8") as f:
    f.write(response.text)

print(f"  Saved → {raw_path}")

df_raw = pd.read_csv(
    raw_path
)

clean_path = os.path.join(RAW_DIR, "euro15_gini_wealth.parquet")


df_raw.to_parquet(clean_path, index=False)

print(f"  Saved → {clean_path}")
