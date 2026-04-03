import pandas as pd
import numpy as np
from scipy import stats
import os

# ============================================
# PHASE 5 — COMPLETE 5 PILLAR ANALYSIS
# Ireland Housing Crisis
# ============================================

print("Loading all datasets...")
rent = pd.read_csv("data/cleaned/rtb_rent_clean.csv")
cso = pd.read_csv("data/cleaned/cso_housing_clean.csv")
hea = pd.read_csv("data/cleaned/hea_enrolment_clean.csv")
census = pd.read_csv("data/raw/census_2022_population.csv")
stress = pd.read_csv("data/cleaned/stress_index.csv")
ip_nationality = pd.read_csv("data/raw/ip_nationality_2024.csv")
ip_backlog = pd.read_csv("data/raw/ip_backlog_2024.csv")
abp = pd.read_csv("data/raw/abp_national.csv")
print(" All datasets loaded!\n")

# ============================================
# PILLAR 1 — RENT GROWTH TRENDS
# Which counties are growing fastest?
# ============================================
print("="*60)
print("PILLAR 1 — RENT GROWTH TRENDS")
print("="*60)

rent_sorted = rent.sort_values(['county', 'year'])
rent_sorted['rent_growth'] = rent_sorted.groupby('county')['avg_monthly_rent'].pct_change() * 100

avg_growth = rent_sorted.groupby('county')['rent_growth'].mean().reset_index()
avg_growth.columns = ['county', 'avg_annual_growth_pct']
avg_growth = avg_growth.sort_values('avg_annual_growth_pct', ascending=False)

print("\nTop 10 counties by average annual rent growth:")
print(avg_growth.head(10).to_string(index=False))

# Overall national rent growth
national_avg_growth = avg_growth['avg_annual_growth_pct'].mean()
print(f"\nNational average annual rent growth: {national_avg_growth:.1f}%")

# Dublin specific
dublin_growth = avg_growth[avg_growth['county'] == 'Dublin']['avg_annual_growth_pct'].values[0]
print(f"Dublin average annual rent growth: {dublin_growth:.1f}%")

# ============================================
# PILLAR 2 — SUPPLY GAP ANALYSIS
# Houses built vs population need
# ============================================
print("\n" + "="*60)
print("PILLAR 2 — SUPPLY GAP ANALYSIS")
print("="*60)

supply = cso.merge(census, on='county', how='inner')
supply['completions_per_1000'] = (
    supply['housing_completions'] / supply['population_2022']
) * 1000

avg_supply = supply.groupby('county')['completions_per_1000'].mean().reset_index()
avg_supply = avg_supply.sort_values('completions_per_1000', ascending=True)

print("\nWorst 10 counties for housing supply (per 1000 people):")
print(avg_supply.head(10).to_string(index=False))

total_built = cso['housing_completions'].sum()
print(f"\nTotal houses built 2019-2024: {total_built:,}")

# ============================================
# PILLAR 3 — STUDENT DEMAND vs RENT
# Does international student growth
# correlate with rent increases?
# ============================================
print("\n" + "="*60)
print("PILLAR 3 — STUDENT DEMAND vs RENT CORRELATION")
print("="*60)

hea['year'] = hea['academic_year'].astype(int)
merged = rent.merge(hea, on=['county', 'year'], how='inner')

# International students vs rent
corr_intl, p_intl = stats.pearsonr(
    merged['international_students'],
    merged['avg_monthly_rent']
)

# Domestic students vs rent
corr_dom, p_dom = stats.pearsonr(
    merged['domestic_students'],
    merged['avg_monthly_rent']
)

print(f"\nInternational students vs rent:")
print(f"  Correlation: {corr_intl:.3f}")
print(f"  P-value: {p_intl:.6f}")
print(f"  Significant: {'YES ' if p_intl < 0.05 else 'NO '}")

print(f"\nDomestic students vs rent:")
print(f"  Correlation: {corr_dom:.3f}")
print(f"  P-value: {p_dom:.6f}")
print(f"  Significant: {'YES ' if p_dom < 0.05 else 'NO '}")

if corr_intl > corr_dom:
    print(f"\n International students have STRONGER correlation with rent than domestic")
else:
    print(f"\n Domestic students have stronger correlation with rent")

# ============================================
# PILLAR 4 — IP/MIGRATION DEMAND PRESSURE
# International protection backlog impact
# ============================================
print("\n" + "="*60)
print("PILLAR 4 — IP/MIGRATION DEMAND PRESSURE")
print("="*60)

total_pending = ip_backlog[ip_backlog['metric'] == 'IPO Pending']['value_dec_2024'].values[0]
wait_weeks = ip_backlog[ip_backlog['metric'] == 'Median Wait Weeks']['value_dec_2024'].values[0]
wait_years = wait_weeks / 52

print(f"\nTotal pending IP applications: {int(total_pending):,}")
print(f"Median wait time: {wait_weeks} weeks ({wait_years:.1f} years)")
print(f"\nTop nationalities applying for protection:")
print(ip_nationality.to_string(index=False))

# Housing demand from backlog
avg_household = 2.75
housing_demand_from_ip = total_pending / avg_household
print(f"\nEstimated housing units needed for IP backlog: {int(housing_demand_from_ip):,}")
print(f"(Assuming average household size of {avg_household})")

# ============================================
# PILLAR 5 — PLANNING SYSTEM FAILURE
# ABP delays killing housing delivery
# ============================================
print("\n" + "="*60)
print("PILLAR 5 — PLANNING SYSTEM FAILURE")
print("="*60)

print("\nPlanning processing times:")
print(abp[['year', 'appeals_received', 'avg_weeks_to_decide', 
            'pct_within_statutory_period']].to_string(index=False))

# Calculate deterioration
start_weeks = abp['avg_weeks_to_decide'].iloc[0]
end_weeks = abp['avg_weeks_to_decide'].iloc[-1]
deterioration = ((end_weeks - start_weeks) / start_weeks) * 100

start_pct = abp['pct_within_statutory_period'].iloc[0]
end_pct = abp['pct_within_statutory_period'].iloc[-1]

print(f"\nProcessing time increase 2019-2023: {deterioration:.0f}%")
print(f"Statutory compliance: {start_pct}% → {end_pct}%")
print(f"Shadow supply (approved but unbuilt): 53,148 units")

# ============================================
# SUMMARY — KEY FINDINGS
# ============================================
print("\n" + "="*60)
print(" SUMMARY — KEY FINDINGS")
print("="*60)

print(f"""
1. RENT GROWTH: National average {national_avg_growth:.1f}% annual growth
   Dublin: {dublin_growth:.1f}% — but rural counties hit harder proportionally

2. SUPPLY GAP: Only {total_built:,} units built 2019-2024
   Critically undersupplied in Leitrim, Longford, Roscommon

3. STUDENT DEMAND: International students correlation with rent = {corr_intl:.3f}
   {'Statistically significant' if p_intl < 0.05 else 'Not significant'} (p={p_intl:.4f})

4. IP PRESSURE: {int(total_pending):,} people waiting {wait_years:.1f} years
   Requiring ~{int(housing_demand_from_ip):,} housing units

5. PLANNING FAILURE: Processing time up {deterioration:.0f}% (2019-2023)
   53,148 approved units never built — systemic delivery failure
""")

# Save summary
os.makedirs("data/cleaned", exist_ok=True)
avg_growth.to_csv("data/cleaned/rent_growth_by_county.csv", index=False)
avg_supply.to_csv("data/cleaned/supply_gap_by_county.csv", index=False)
print(" Analysis complete! Results saved.")