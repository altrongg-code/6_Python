"""
    Matplotlib 으로 차트 생성
"""
import matplotlib

matplotlib.use('Agg')
# Agg (Anti-Grain Geomatry)
# : 화면(GUI 창)을 열지 않고, 메모리 내에서만 차트 표시(렌더링)
#   화면에 따로 출력하지 않고 파일로 저장할 때 설정
# * pyplot 임포트 하기 전에 설정해야 함!

import matplotlib.pyplot as plt

from chart_config import setup, out
from merged_loader import load_merged

setup()
df = load_merged()

one = df[df['code'] == 'G0001'].sort_values('date')

# Figure, Axes
#   - Figure (도화지) =>  Axes (그래프 하나)

# * subplots(행, 열, figsizes=(가로, 세로))
# 행, 열 생략 시 1 * 1

fig, ax = plt.subplots(figsize=(12,4))
# figsize => 14*4.  dpi(100) --> 1200 * 400.

# ax.plot(x, y)
ax.plot(one['date'], one['close'])

ax.set_title("가온전자 주가 추이")
ax.set_xlabel('날짜')
ax.set_ylabel('종가(원)')
ax.grid(alpha=0.3)

fig.savefig(out('01_basic.png'))
