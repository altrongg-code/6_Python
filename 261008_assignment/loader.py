"""
    데이터 로드
"""
import pandas as pd
from config import ENCODING, path

def load_rentals():
    """clean_rentals.csv 파일을 읽어서 DF 반환"""
    return pd.read_csv(path('clean_rentals.csv'), encoding=ENCODING, parse_dates=['rent_time', 'return_time'])

def load_users():
    """users.csv 파일을 읽어서 DF 반환"""
    return pd.read_csv(path('users.csv'), encoding=ENCODING)
