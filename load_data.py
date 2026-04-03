import pandas as pd
from sqlalchemy import create_engine
import os

# ============================================
# LOAD CLEANED DATA INTO POSTGRESQL
# ============================================

# -----------------------------------------------
# CONNECTION STRING
# This tells Python how to connect to PostgreSQL
# Format: postgresql://username@host/database
# -----------------------------------------------
engine = create_engine('postgresql://poojasharma@localhost/housing_crisis_ireland')

print(" Connected to PostgreSQL!")

# -----------------------------------------------
# LOAD RENT PRICES
# -----------------------------------------------
print("\n Loading rent prices...")
rent = pd.read_csv("data/cleaned/rtb_rent_clean.csv")
rent.to_sql('rent_prices', engine, if_exists='replace', index=False)
print(f" Loaded {len(rent)} rows into rent_prices")

# -----------------------------------------------
# LOAD HOUSING COMPLETIONS
# -----------------------------------------------
print("\n Loading housing completions...")
cso = pd.read_csv("data/cleaned/cso_housing_clean.csv")
cso.to_sql('housing_completions', engine, if_exists='replace', index=False)
print(f" Loaded {len(cso)} rows into housing_completions")

# -----------------------------------------------
# LOAD STUDENT ENROLMENT
# -----------------------------------------------
print("\n Loading student enrolment...")
hea = pd.read_csv("data/cleaned/hea_enrolment_clean.csv")
hea.to_sql('student_enrolment', engine, if_exists='replace', index=False)
print(f" Loaded {len(hea)} rows into student_enrolment")

# -----------------------------------------------
# LOAD CENSUS POPULATION
# -----------------------------------------------
print("\n Loading census population...")
census = pd.read_csv("data/raw/census_2022_population.csv")
census.to_sql('census_population', engine, if_exists='replace', index=False)
print(f" Loaded {len(census)} rows into census_population")

print("\n All data loaded successfully!")
print("Database is ready for analysis!")