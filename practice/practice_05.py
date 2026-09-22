import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pathlib import Path

from chart_config import setup, out

setup()

# 데이터 로드
data_path = Path(__file__).with_name("business_data.csv")
if not data_path.exists():
    data_path = Path("business_data.csv")

df = pd.read_csv(data_path, parse_dates=["game_date"])

# 시각화
fig, ax = plt.subplots(figsize=(9, 5))
df_hits_clean = df.dropna(subset=["hits"])

sns.barplot(
    data=df_hits_clean,
    x="team",
    y="hits",
    hue="team",
    errorbar="sd",
    palette="viridis",
    legend=False,
    ax=ax,
)

ax.set_title("팀별 경기당 평균 안타 수")
ax.set_xlabel("팀 이름")
ax.set_ylabel("평균 안타 수 (개)")
ax.grid(alpha=0.3)

for container in ax.containers:
    ax.bar_label(container, fmt="%.2f", padding=3, fontsize=9)

plt.tight_layout()
fig.savefig(out('team_hit_mean'), dpi=120)
plt.close(fig)
print(f"✅ 차트 저장 완료")




# ---------------------------------------------------------
# 과제 2: 피안타/안타 트레이드오프와 승패 분기점 산점도
# ---------------------------------------------------------

teams = df['team'].unique().tolist()
print(teams)

fig, axes = plt.subplots(2, 2, figsize=(11, 10))

for ax, team in zip(axes.flatten(), teams):
    sub_df = df[df['team'] == team]
    ax.scatter(sub_df['hits'], sub_df['runs_scored'], s=10, alpha=0.75, color='steelblue')
    
    ax.set_title(f"{team} (안타 vs 낸 점수)")
    ax.set_xlabel("안타 수")
    ax.set_ylabel("낸 점수")
    ax.grid(True, linestyle='--', alpha=0.4)

fig.tight_layout()
fig.savefig(out('hit_run_scatter.png'), dpi=120)
plt.close(fig)
print("✅ 차트 저장 완료")

fig, axes = plt.subplots(2, 2, figsize=(11, 10))

for ax, team in zip(axes.flatten(), teams):
    sub_df = df[df['team'] == team]
    ax.scatter(sub_df['allowed_hits'], sub_df['runs_allowed'], s=10, alpha=0.75, color='steelblue')
    
    ax.set_title(f"{team} (피안타 vs 실점 수)")
    ax.set_xlabel("피안타 수")
    ax.set_ylabel("실점 수")
    ax.grid(True, linestyle='--', alpha=0.4)

fig.tight_layout()
fig.savefig(out('allowed_hit_run_scatter.png'), dpi=120)
plt.close(fig)
print("✅ 차트 저장 완료")


# ---------------------------------------------------------
# 과제 3: 수비 불안정성 세그먼트 비교 (박스플롯)
# ---------------------------------------------------------

fig, ax = plt.subplots(figsize=(13,5))

sns.boxplot(data=df, x="team", y="errors", ax=ax)

ax.set_title("팀별 실책 분포 및 IQR 확인")
ax.set_xlabel("팀")
ax.set_ylabel("실책 수")

ax.tick_params(axis="x", rotation=15)

fig.savefig(out("team_errors_box.png"), dpi=120)
plt.close(fig)


per_team = 0

for name, g in df.groupby('team'):
    a,b = g['errors'].quantile([0.25, 0.75])
    i = b - a

    per_team += ((g['errors'] < a - 1.5 * i) | (g['errors'] > b + 1.5 * i)).sum()

print(f"팀별 이상치 합 : {per_team:,}건")



# ---------------------------------------------------------
# 과제 4: 피벗 테이블 생성: 팀 x 수비 세그먼트(0, 1~3, 4~)별 평균 실점
# ---------------------------------------------------------
def classify_def_tier(x):
    if pd.isna(x):
        return "결측"
    elif x == 0:
        return "0개"
    elif x <= 2:
        return "1개~2개"
    else:
        return "3개 이상"

df['def_tier'] = df['errors'].apply(classify_def_tier)

pivot_df = df.pivot_table(
    index='team', 
    columns='def_tier', 
    values='runs_allowed', 
    aggfunc='mean'
)[['0개', '1개~2개', '3개 이상']]  # 컬럼 순서 정렬

fig, ax = plt.subplots(figsize=(9, 5))
sns.heatmap(pivot_df, annot=True, fmt=".2f", cmap="YlOrRd", cbar_kws={'label': '평균 실점'}, ax=ax)
ax.set_title("팀별 수비 티어(실책 수)에 따른 평균 실점 히트맵")
ax.set_xlabel("수비 세그먼트")
ax.set_ylabel("팀")
fig.tight_layout()
fig.savefig(out("team_def_tier_heatmap.png"), dpi=120)
plt.close(fig)

