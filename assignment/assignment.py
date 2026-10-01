import matplotlib

matplotlib.use('Agg')

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from config import path, ENCODING
from chart_config import setup, out

setup()

df = pd.read_csv(path('train.csv'), encoding=ENCODING)

df.info()

print(df.head(5))
