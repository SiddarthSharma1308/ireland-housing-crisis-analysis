import pandas as pd

# Non-Irish student enrollment from HEA dashboard
# Source: hea.ie - Domicile filter: All except Republic of Ireland
hea_international = {
    'academic_year': [
        '2007/2008','2008/2009','2009/2010','2010/2011','2011/2012',
        '2012/2013','2013/2014','2014/2015','2015/2016','2016/2017',
        '2017/2018','2018/2019','2019/2020','2020/2021','2021/2022',
        '2022/2023','2023/2024','2024/2025'
    ],
    'non_irish_enrolled': [
        13700, 14735, 14635, 15280, 13700,
        15670, 19085, 21105, 23710, 24720,
        26470, 29080, 29855, 26785, 31720,
        35140, 40400, 44535
    ]
}

df = pd.DataFrame(hea_international)
baseline = 23710  # 2015/16
df['increase_from_2015'] = df['non_irish_enrolled'] - baseline
df['pct_increase_from_2015'] = ((df['non_irish_enrolled'] - baseline) / baseline * 100).round(1)

df.to_csv('data/cleaned/hea_international_enrollment_2007_2025.csv', index=False)
print(df.to_string(index=False))
print(f"\nIncrease 2015/16 to 2024/25: {44535 - 23710:,} students (+{((44535-23710)/23710*100):.1f}%)")