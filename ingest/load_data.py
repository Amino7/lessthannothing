"""
load_raw.py
-----------
Step 1: Fetch raw data from Eurostat API and save to data/raw/

Run from project root:
    python scripts/load_raw.py
"""

import os
import requests

RAW_DIR = os.path.join("data", "raw")
os.makedirs(RAW_DIR, exist_ok=True)

BASE_URL = "https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data"

datasets = {
    "ilc_di12_gini": "ilc_di12",       # Gini coefficient
    "ilc_di01_quintiles": "ilc_di01",  # Income shares by quintile
    "ilc_di11_s80s20": "ilc_di11",     # S80/S20 ratio
}

params = {
    "format": "TSV",
    "compressed": "false",
}

for filename, dataset_code in datasets.items():
    print(f"Fetching {dataset_code}...")
    response = requests.get(f"{BASE_URL}/{dataset_code}", params=params, timeout=60)
    print(f"  Status: {response.status_code}")

    raw_path = os.path.join(RAW_DIR, f"{filename}.tsv")
    with open(raw_path, "w", encoding="utf-8") as f:
        f.write(response.text)
    print(f"  Saved → {raw_path}")

print("\nDone.")