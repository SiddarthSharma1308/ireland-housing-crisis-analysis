import pandas as pd

ip_data = {
    'nationality': ['Nigeria', 'Jordan', 'Pakistan', 'Somalia', 'Bangladesh', 'Other'],
    'pct_applications_2024': [21.7, 15.5, 7.5, 7.0, 5.4, 42.8],
    'pending_ipo': [22548],
    'median_wait_weeks': [79.5]
}

# Top nationalities as percentage
nationality_df = pd.DataFrame({
    'nationality': ['Nigeria', 'Jordan', 'Pakistan', 'Somalia', 'Bangladesh', 'Other'],
    'pct_2024': [21.7, 15.5, 7.5, 7.0, 5.4, 42.8]
})

# System backlog metrics
backlog_df = pd.DataFrame({
    'metric': ['IPO Pending', 'IPAT Pending Appeals', 'Median Wait Weeks'],
    'value_dec_2024': [22548, 9243, 79.5]
})

nationality_df.to_csv("data/raw/ip_nationality_2024.csv", index=False)
backlog_df.to_csv("data/raw/ip_backlog_2024.csv", index=False)

print(" Saved ip_nationality_2024.csv")
print(nationality_df)
print("\n Saved ip_backlog_2024.csv")
print(backlog_df)