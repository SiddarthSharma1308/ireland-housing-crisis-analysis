import pandas as pd
import os

# ============================================
# CLEAN RTB RENT DATA
# ============================================

# Load raw data
df = pd.read_csv("data/raw/rtb_rent_prices.csv")
print(f"Raw shape: {df.shape}")

# -----------------------------------------------
# STEP 1 — Filter to 'All bedrooms' and 
# 'All property types' only
# We want overall county averages, not broken
# down by bedroom count or property type
# -----------------------------------------------
df = df[df['Number of Bedrooms'] == 'All bedrooms']
df = df[df['Property Type'] == 'All property types']
print(f"After bedroom/property filter: {df.shape}")

# -----------------------------------------------
# STEP 2 — Filter years 2019 to 2024
# Matches our other datasets' time range
# -----------------------------------------------
df = df[df['Year'] >= 2019]
print(f"After year filter: {df.shape}")

# -----------------------------------------------
# STEP 3 — Filter to county level only
# We only want the 26 county names, not towns
# -----------------------------------------------
irish_counties = [
    'Carlow', 'Cavan', 'Clare', 'Cork', 'Donegal',
    'Dublin', 'Galway', 'Kerry', 'Kildare', 'Kilkenny',
    'Laois', 'Leitrim', 'Limerick', 'Longford', 'Louth',
    'Mayo', 'Meath', 'Monaghan', 'Offaly', 'Roscommon',
    'Sligo', 'Tipperary', 'Waterford', 'Westmeath', 'Wexford',
    'Wicklow'
]

df = df[df['Location'].isin(irish_counties)]
print(f"After county filter: {df.shape}")

# -----------------------------------------------
# STEP 4 — Drop useless columns
# 'STATISTIC Label' always says the same thing
# 'UNIT' always says 'Euro'
# 'Number of Bedrooms' and 'Property Type' 
# are now redundant after filtering
# -----------------------------------------------
df = df.drop(columns=[
    'STATISTIC Label', 
    'UNIT',
    'Number of Bedrooms',
    'Property Type'
])
print(f"After dropping columns: {df.shape}")

# -----------------------------------------------
# STEP 5 — Handle missing VALUES
# Drop rows where rent value is null
# These are genuinely missing data points
# not zeros — we can't impute rent prices
# -----------------------------------------------
print(f"\nMissing values before: {df['VALUE'].isnull().sum()}")
df = df.dropna(subset=['VALUE'])
print(f"Missing values after: {df['VALUE'].isnull().sum()}")

# -----------------------------------------------
# STEP 6 — Rename columns to clean names
# -----------------------------------------------
df = df.rename(columns={
    'Location': 'county',
    'Year': 'year',
    'VALUE': 'avg_monthly_rent'
})

# -----------------------------------------------
# STEP 7 — Final check
# -----------------------------------------------
print(f"\nFinal shape: {df.shape}")
print(f"\nSample cleaned data:")
print(df.head(10))
print(f"\nMissing values in final data:")
print(df.isnull().sum())

# -----------------------------------------------
# STEP 8 — Save cleaned file
# -----------------------------------------------
os.makedirs("data/cleaned", exist_ok=True)
df.to_csv("data/cleaned/rtb_rent_clean.csv", index=False)
print(f"\n✅ Saved to data/cleaned/rtb_rent_clean.csv")