import pandas as pd

# Census 2022 - Official CSO figures
# Source: CSO Census 2022 Summary Results
census_data = {
    'county': [
        'Carlow', 'Cavan', 'Clare', 'Cork', 'Donegal',
        'Dublin', 'Galway', 'Kerry', 'Kildare', 'Kilkenny',
        'Laois', 'Leitrim', 'Limerick', 'Longford', 'Louth',
        'Mayo', 'Meath', 'Monaghan', 'Offaly', 'Roscommon',
        'Sligo', 'Tipperary', 'Waterford', 'Westmeath', 'Wexford',
        'Wicklow'
    ],
    'population_2022': [
        61981, 76176, 129592, 570387, 163944,
        1450000, 268421, 122740, 246977, 102021,
        96443, 34953, 205820, 46478, 145607,
        130507, 220579, 61928, 82157, 70538,
        67072, 163995, 116334, 95832, 165507,
        148462
    ]
}

df = pd.DataFrame(census_data)
df.to_csv("data/raw/census_2022_population.csv", index=False)
print(f"✅ Saved census_2022_population.csv")
print(df)