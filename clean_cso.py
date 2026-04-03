import pandas as pd
import os

# ============================================
# CLEAN CSO HOUSING COMPLETIONS DATA
# ============================================

df = pd.read_csv("data/raw/cso_housing_completions.csv")
print(f"Raw shape: {df.shape}")
print(df.head(3))

# -----------------------------------------------
# STEP 1 — Strip 'County Council' and 
# 'City Council' from location names
# So they match our other datasets
# -----------------------------------------------
df['Local Authority'] = df['Local Authority'].str.replace(' County Council', '')
df['Local Authority'] = df['Local Authority'].str.replace(' City Council', '')
df['Local Authority'] = df['Local Authority'].str.replace(' City and County Council', '')

print(f"\nUnique locations after cleaning:")
print(df['Local Authority'].unique())

# -----------------------------------------------
# STEP 2 — Extract year from Quarter column
# 'Quarter' currently looks like '2019Q1'
# We extract just the year '2019'
# -----------------------------------------------
df['year'] = df['Quarter'].str[:4].astype(int)
# str[:4] means take first 4 characters
# astype(int) converts '2019' string to 2019 number

# -----------------------------------------------
# STEP 3 — Filter years 2019 to 2024
# -----------------------------------------------
df = df[df['year'] >= 2019]
print(f"\nAfter year filter: {df.shape}")

# -----------------------------------------------
# STEP 4 — Filter to 'All house types' only
# So we get total completions per county
# not broken down by house type
# -----------------------------------------------
print(f"\nUnique house types:")
print(df['Type of House'].unique())

df = df[df['Type of House'] == 'All house types']
print(f"After house type filter: {df.shape}")

# -----------------------------------------------
# STEP 5 — Aggregate quarterly to yearly
# Sum up all 4 quarters per county per year
# -----------------------------------------------
df = df.groupby(['Local Authority', 'year'])['VALUE'].sum().reset_index()
# groupby → group rows by county and year
# ['VALUE'].sum() → add up completions per group
# reset_index() → converts back to normal dataframe

print(f"\nAfter yearly aggregation: {df.shape}")

# -----------------------------------------------
# STEP 6 — Rename columns
# -----------------------------------------------
df = df.rename(columns={
    'Local Authority': 'county',
    'VALUE': 'housing_completions'
})

# -----------------------------------------------
# STEP 7 — Final check
# -----------------------------------------------
print(f"\nFinal shape: {df.shape}")
print(f"\nSample cleaned data:")
print(df.head(10))
print(f"\nMissing values:")
print(df.isnull().sum())

# -----------------------------------------------
# STEP 8 — Save
# -----------------------------------------------
os.makedirs("data/cleaned", exist_ok=True)
df.to_csv("data/cleaned/cso_housing_clean.csv", index=False)
print(f"\n Saved to data/cleaned/cso_housing_clean.csv")