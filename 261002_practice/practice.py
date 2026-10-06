import pandas as pd
import numpy as np
import unicodedata

from config import path, ENCODING

stations = pd.read_csv(path('stations.csv'), encoding=ENCODING, keep_default_na=False)
raw_bikes = pd.read_csv(path('raw-bikes.csv'), encoding=ENCODING, keep_default_na=False)
raw_rentals = pd.read_csv(path('raw-rentals.csv'), encoding=ENCODING, keep_default_na=False)

stations.info()
print()

raw_bikes.info()
print()

raw_rentals.info()
print()

raw_bikes_str = pd.read_csv(path('raw-bikes.csv'), encoding=ENCODING, keep_default_na=False, dtype=str)
raw_rentals_str = pd.read_csv(path('raw-rentals.csv'), encoding=ENCODING, keep_default_na=False, dtype=str)

print(raw_bikes_str['bike_id'].nunique())   # 50행

# station_id — 대문자로 통일, 빈 값은 결측으로 처리
raw_bikes_str['station_id'] = raw_bikes_str['station_id'].str.upper().replace(r'^\s*$', np.nan, regex=True)

print(raw_bikes_str['bike_type'].unique())

# bike_type — 일반 / 전동 두 가지로 통일
raw_bikes_str['bike_type'] = raw_bikes_str['bike_type'].apply(
    lambda x: unicodedata.normalize("NFKC", str(x)) if pd.notnull(x) else x
)

raw_bikes_str['bike_type'] = (
    raw_bikes_str['bike_type']
    .str.replace(' ', '')
    .replace({
        '일반형': '일반',
        'electric': '전동'
    })
)

# gear_count — 단위 문자를 제거하고 정수로
raw_bikes_str['gear_count'] = pd.to_numeric(raw_bikes_str['gear_count'].str.replace('단', ''), errors='coerce')

# daily_fee — 콤마 제거 후 정수로
raw_bikes_str['daily_fee'] = pd.to_numeric(raw_bikes_str['daily_fee'].str.replace(',', ''), errors='coerce')

# manufacture_year — 정수로 (변환 실패는 결측으로)
raw_bikes_str['manufacture_year'] = pd.to_numeric(raw_bikes_str['manufacture_year'], errors='coerce')

# 중복 제거 — bike_id 기준
raw_bikes_str = raw_bikes_str.drop_duplicates(subset='bike_id', keep='first').reset_index(drop=True)

print(len(raw_bikes_str))
print(raw_bikes_str['bike_type'].unique())
print(raw_bikes_str['station_id'].sort_values().unique())
print(raw_bikes_str['gear_count'].unique())
print(f"{raw_bikes_str['daily_fee'].min()} ~ {raw_bikes_str['daily_fee'].max()}")

# distance_km, fee — 콤마 제거 후 숫자로. 변환 실패는 결측으로
cols_to_numeric = ['distance_km', 'fee']

for col in cols_to_numeric:
    raw_rentals_str[col] = pd.to_numeric(
        raw_rentals_str[col].str.replace(',', ''), 
        errors='coerce'
    )

cols_to_datetime = ['rent_time', 'return_time']

# rent_time, return_time — datetime 으로 통일 (형식 3종 혼재)
for col in cols_to_datetime:
    raw_rentals_str[col] = pd.to_datetime(raw_rentals_str[col], format='mixed', errors='coerce')

# payment_method — 공백 제거 후 대문자로 통일
raw_rentals_str['payment_method'] = raw_rentals_str['payment_method'].str.replace(' ', '').str.upper()

# 중복 제거 — rental_id 기준
raw_rentals_str = raw_rentals_str.drop_duplicates(subset='rental_id', keep='first').reset_index(drop=True)

print(len(raw_rentals_str))
print(raw_rentals_str['distance_km'].isna().sum())
print(raw_rentals_str['fee'].isna().sum())
print(raw_rentals_str['payment_method'].unique())
