import pandas as pd
from sqlalchemy import create_engine

engine = create_engine('postgresql://poojasharma@localhost/housing_crisis_ireland')

# ============================================
# HOUSING STRESS INDEX
# Combines 3 metrics into one score per county
# 1. Rent level (affordability)
# 2. Supply gap (completions vs population)
# 3. Rent growth (year on year change)
# ============================================

query = """
WITH rent_growth AS (
    SELECT 
        county,
        year,
        avg_monthly_rent,
        LAG(avg_monthly_rent) OVER (
            PARTITION BY county 
            ORDER BY year
        ) as prev_year_rent,
        ROUND(CAST(
            (avg_monthly_rent - LAG(avg_monthly_rent) OVER (
                PARTITION BY county ORDER BY year
            )) / NULLIF(LAG(avg_monthly_rent) OVER (
                PARTITION BY county ORDER BY year
            ), 0) * 100 AS NUMERIC), 2
        ) as rent_growth_pct
    FROM rent_prices
),
combined AS (
    SELECT 
        r.county,
        r.year,
        r.avg_monthly_rent,
        r.rent_growth_pct,
        h.housing_completions,
        c.population_2022,
        ROUND(CAST(
            r.avg_monthly_rent / NULLIF(h.housing_completions, 0) 
        AS NUMERIC), 2) as supply_pressure
    FROM rent_growth r
    JOIN housing_completions h ON r.county = h.county AND r.year = h.year
    JOIN census_population c ON r.county = c.county
    WHERE r.year >= 2020
)
SELECT 
    county,
    year,
    avg_monthly_rent,
    rent_growth_pct,
    housing_completions,
    supply_pressure,
    ROUND(CAST(
        (avg_monthly_rent / 500) + 
        COALESCE(rent_growth_pct, 0) + 
        (supply_pressure / 2)
    AS NUMERIC), 2) as stress_index
FROM combined
ORDER BY stress_index DESC
LIMIT 15;
"""

df = pd.read_sql(query, engine)
print(" HOUSING STRESS INDEX — TOP 15 COUNTIES")
print("="*60)
print(df.to_string(index=False))

df.to_csv("data/cleaned/stress_index.csv", index=False)
print("\n Saved to data/cleaned/stress_index.csv")