import pandas as pd
import glob
import os

# ============================================
# CLEAN HEA ENROLMENT DATA
# ============================================

# -----------------------------------------------
# STEP 1 — Load and combine all 7 yearly files
# glob finds all files matching a pattern
# * means "anything can go here"
# -----------------------------------------------
all_files = glob.glob("data/raw/hea_enrolment_*.csv")
print(f"Found {len(all_files)} HEA files:")
print(all_files)

frames = []
for file in all_files:
    df_temp = pd.read_csv(file)
    year = file.split('_')[-2]
    df_temp['academic_year'] = year
    frames.append(df_temp)

df = pd.concat(frames, ignore_index=True)
print(f"\nCombined shape: {df.shape}")
print(df.head(3))

# -----------------------------------------------
# STEP 2 — Drop parent university rows
# These are summary rows with no campus name
# Institute column is null for these rows
# -----------------------------------------------
df = df.dropna(subset=['Institute'])
print(f"\nAfter dropping parent rows: {df.shape}")

# -----------------------------------------------
# STEP 3 — Create international students column
# International = EU + Non-EU + GB + NI
# -----------------------------------------------
df['international_students'] = (
    df['(Other) EU'] +
    df['Non-EU'] +
    df['Great Britain'] +
    df['Northern Ireland']
)
df['domestic_students'] = df['Ireland']

print(f"\nSample with new columns:")
print(df[['Institute', 'academic_year', 'domestic_students', 'international_students']].head(5))

# -----------------------------------------------
# STEP 4 — Map institutes to counties
# -----------------------------------------------
institute_to_county = {
    'ATU Donegal': 'Donegal',
    'ATU Galway-Mayo': 'Galway',
    'ATU Sligo': 'Sligo',
    'ATU Mayo': 'Mayo',
    'Cork IT': 'Cork',
    'MTU Cork': 'Cork',
    'MTU Kerry': 'Kerry',
    'TU Dublin': 'Dublin',
    'TU Dublin - Blanchardstown Campus': 'Dublin',
    'TU Dublin - Tallaght Campus': 'Dublin',
    'DCU': 'Dublin',
    'UCD': 'Dublin',
    'TCD': 'Dublin',
    'RCSI': 'Dublin',
    'NCAD': 'Dublin',
    'DIT': 'Dublin',
    'UCC': 'Cork',
    'UL': 'Limerick',
    'LIT': 'Limerick',
    'TUS Limerick': 'Limerick',
    'TUS Midlands': 'Offaly',
    'University of Galway': 'Galway',
    'NUI Galway': 'Galway',
    'NUIG': 'Galway',
    'Maynooth University': 'Kildare',
    'IT Carlow': 'Carlow',
    'SETU Carlow': 'Carlow',
    'SETU Waterford': 'Waterford',
    'WIT': 'Waterford',
    'IT Tralee': 'Kerry',
    'IT Sligo': 'Sligo',
    'GMIT': 'Galway',
    'LYIT': 'Donegal',
    'DkIT': 'Louth',
    'IT Tallaght': 'Dublin',
    'IT Blanchardstown': 'Dublin',
    'Mater Dei': 'Dublin',
    'St Patricks College': 'Dublin',
    'Dublin City University': 'Dublin',
    'Dun Laoghaire Institute of Art, Design and Technology': 'Dublin',
    'Dundalk IT': 'Louth',
    'Mary Immaculate College, Limerick': 'Limerick',
    'National College of Art and Design': 'Dublin',
    'National College of Ireland': 'Dublin',
    'Royal College of Surgeons': 'Dublin',
    'St. Angelas College of Home Economics, Sligo': 'Sligo',
    'TU Dublin Blanchardstown': 'Dublin',
    'TU Dublin City': 'Dublin',
    'TU Dublin Tallaght': 'Dublin',
    'TUS Athlone': 'Westmeath',
    'Trinity College Dublin': 'Dublin',
    'University College Cork': 'Cork',
    'University College Dublin': 'Dublin',
    'University of Limerick': 'Limerick',
}

df['county'] = df['Institute'].map(institute_to_county)

unmapped = df[df['county'].isna()]['Institute'].unique()
print(f"\nUnmapped institutes ({len(unmapped)}):")
print(unmapped)

# -----------------------------------------------
# STEP 5 — Drop unmapped rows
# -----------------------------------------------
df = df.dropna(subset=['county'])
print(f"\nAfter dropping unmapped: {df.shape}")

# -----------------------------------------------
# STEP 6 — Keep only columns we need
# -----------------------------------------------
df = df[['county', 'academic_year', 'domestic_students',
         'international_students', 'Row_Total']]
df = df.rename(columns={'Row_Total': 'total_students'})

# -----------------------------------------------
# STEP 7 — Aggregate by county and year
# Multiple campuses in same county get summed
# -----------------------------------------------
df = df.groupby(['county', 'academic_year']).sum().reset_index()
print(f"\nAfter county aggregation: {df.shape}")

# -----------------------------------------------
# STEP 8 — Final check and save
# -----------------------------------------------
print(f"\nSample cleaned data:")
print(df.head(10))
print(f"\nMissing values:")
print(df.isnull().sum())

os.makedirs("data/cleaned", exist_ok=True)
df.to_csv("data/cleaned/hea_enrolment_clean.csv", index=False)
print(f"\n Saved to data/cleaned/hea_enrolment_clean.csv")