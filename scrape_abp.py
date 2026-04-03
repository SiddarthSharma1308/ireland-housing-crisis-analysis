import requests
import pandas as pd
import os

# ============================================
# SCRAPE AN BORD PLÁNÁLA PLANNING DATA
# ============================================

headers = {"User-Agent": "Mozilla/5.0"}

years = [2019, 2020, 2021, 2022, 2023]
all_data = []

for year in years:
    print(f" Scraping ABP data for {year}...")
    
    url = f"https://www.pleanala.ie/en-ie/publications/annual-reports/{year}"
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        tables = pd.read_html(response.text)
        
        print(f"Found {len(tables)} tables for {year}")
        
        # Table 3 — Planning Appeals
        if len(tables) >= 3:
            df = tables[2]
            df['year'] = year
            all_data.append(df)
            print(f" Got planning appeals table for {year}")
        
    except Exception as e:
        print(f" Failed for {year}: {e}")

if all_data:
    combined = pd.concat(all_data, ignore_index=True)
    os.makedirs("data/raw", exist_ok=True)
    combined.to_csv("data/raw/abp_planning.csv", index=False)
    print(f"\n Saved abp_planning.csv — {len(combined)} rows")
else:
    print("\n No data scraped — will use manual approach")