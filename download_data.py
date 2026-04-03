import pandas as pd
import requests
import os

os.makedirs("data/raw", exist_ok=True)

# -----------------------------------------------
# DATASET 4 — Census 2022 Population by County
# -----------------------------------------------
print("📥 Downloading Census 2022 population...")

# We add headers to pretend we're a real browser
# Some websites block automated requests without this
headers = {"User-Agent": "Mozilla/5.0"}

response = requests.get(
    "https://en.wikipedia.org/wiki/List_of_counties_of_Ireland_by_population",
    headers=headers
)

tables = pd.read_html(response.text)
census = tables[0]

print(f"Columns: {census.columns.tolist()}")
print(census.head(3))

census.to_csv("data/raw/census_2022_population.csv", index=False)
print(f"✅ Saved! {len(census)} rows\n")

print("🎉 Done! Check data/raw/")