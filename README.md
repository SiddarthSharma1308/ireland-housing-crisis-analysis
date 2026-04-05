# 🏠 Ireland Housing Crisis Analysis

A data-driven, multi-pillar analysis of Ireland's private rental market crisis. Built with Python, Streamlit, and Plotly — designed to surface the structural forces driving unaffordability beyond surface-level supply arguments.

---

## 📊 Key Findings

### Pillar 1 — Rent Inflation (RTB Data)
> **Every single county in Ireland saw rents more than double between 2015 and 2025.**

Analysis of 372,000+ RTB tenancy records (2007–2025Q3) across all 26 counties reveals:

| Finding | Detail |
|--------|---------|
| 🔴 Highest increase | Longford: **+170%** (€422 → €1,140/month) |
| 🔴 Galway increase | **+119.5%** (€757 → €1,662/month) |
| 🔴 Dublin increase | **+78.5%** (€1,218 → €2,173/month) — lowest % but highest absolute rent |
| 🟡 National pattern | Crisis has spread far beyond Dublin — traditionally low-cost counties now seeing steepest rises |

*Source: RTB Average Monthly Rent Report via CSO API (RIQ02), 2015Q1 vs 2025Q3*

---

### Pillar 2 — Student Demand Displacement (HEA Data)
> **Non-Irish student enrollment grew +87.8% between 2015 and 2025 — adding 20,825 students who all compete directly in the private rental market.**

| Year | Non-Irish Students | Change vs 2015 |
|------|-------------------|----------------|
| 2015/2016 | 23,710 | baseline |
| 2018/2019 | 29,080 | +22.6% |
| 2021/2022 | 31,720 | +33.8% |
| 2024/2025 | 44,535 | **+87.8%** |

**The correlation:** In the same period Galway rents rose +119.5%, non-Irish enrollment at Irish universities grew +87.8% — students who cannot live at home and must enter the private rental market.

*Source: HEA Enrolled Students Dashboard, Domicile filter: non-Republic of Ireland (2024/25)*

---

## 📋 Project Overview

This project investigates four systemic drivers of Ireland's housing crisis using public datasets from RTB, CSO, HEA, An Bord Plánála, and Census 2022:

| Pillar | Status | Focus |
|--------|--------|-------|
| **Rent Trend Analysis** | ✅ Complete | County-level rent inflation across all 26 counties, 2007–2025 |
| **Student Demand Displacement** | ✅ Complete | Non-Irish enrollment growth vs rent inflation, 2015–2025 |
| **Planning System Paralysis** | 🔄 In progress | An Bord Plánála approval rates, timelines, and bottlenecks |
| **Institutional Landlord Consolidation** | 🔄 In progress | REITs and large-scale landlord market concentration trends |

---

## 🛠️ Tech Stack

- **Python** — data collection, cleaning, and analysis
- **Streamlit** — interactive 7-page dashboard
- **Plotly** — interactive visualisations
- **Pandas** — data wrangling

---

## 📁 Project Structure

```
ireland-housing-crisis-analysis/
│
├── data/
│   ├── raw/
│   │   └── rtb_rent.csv                          # 372,000+ RTB tenancy records (2007–2025Q3)
│   └── cleaned/
│       ├── county_rent_increase_2015_2025.csv     # County-level % rent increase analysis
│       └── hea_international_enrollment_2007_2025.csv  # Non-Irish student enrollment trends
│
├── dashboard.py      # Main Streamlit dashboard (7 pages)
├── fetch_rtb.py      # RTB data ingestion via CSO API
├── fetch_hea.py      # HEA student enrollment data
├── analysis.py       # Core analytical logic
├── download_data.py  # Data ingestion scripts
├── load_data.py      # Data loading utilities
├── explore_data.py   # EDA scripts
│
├── clean_cso.py      # CSO data cleaning
├── clean_hea.py      # HEA data cleaning
├── clean_rent.py     # RTB rent data cleaning
│
├── census_data.py    # Census 2022 processing
├── abp_data.py       # An Bord Plánála data processing
├── scrape_abp.py     # ABP planning data scraper
├── ip_data.py        # Institutional/investor landlord data
├── stress_index.py   # Composite rental stress index
│
└── .gitignore
```

---

## 📂 Data Sources

| Source | Description |
|--------|-------------|
| [RTB](https://www.rtb.ie) | Residential Tenancies Board — rent index and tenancy data |
| [CSO](https://www.cso.ie) | Central Statistics Office — housing and demographic data |
| [HEA](https://www.hea.ie) | Higher Education Authority — student enrollment data |
| [An Bord Plánála](https://www.abp.ie) | National planning appeals data |
| [Census 2022](https://www.census.ie) | Population and household composition data |
| Department of Integration | Refugee and International Protection accommodation data |

---

## 🚀 Running the Dashboard

```bash
# Clone the repository
git clone https://github.com/SiddarthSharma1308/ireland-housing-crisis-analysis.git
cd ireland-housing-crisis-analysis

# Install dependencies
pip install streamlit pandas plotly

# Run the dashboard
streamlit run dashboard.py
```

---

## 👤 Author

**Siddarth Sharma**  
MSc Business Analytics — University of Galway (2025)

[LinkedIn](https://linkedin.com/in/siddarth-sharma2000) | [GitHub](https://github.com/SiddarthSharma1308)
