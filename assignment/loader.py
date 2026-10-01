"""
    데이터 로드
"""
import pandas as pd
from config import ENCODING, path

def load_prices():
    """prices.csv 파일을 읽어서 DF 반환"""
    return pd.read_csv(path('prices.csv'), encoding=ENCODING, parse_dates=['date'])

