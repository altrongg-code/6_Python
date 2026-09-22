import numpy as np
import pandas as pd

np.random.seed(2026)
n_rows = 300  # 샘플 수

dates = pd.date_range(start="2025-04-01", end="2025-09-30", periods=n_rows)
team_list = ["서울 타이거즈", "부산 이글스", "인천 호크스", "대구 라이온스"]
teams = np.random.choice(team_list, size=n_rows)

# 1. 팀별 능력치(스펙) 격차 설정
team_stats = {
    "서울 타이거즈": {"hit_lam": 13.0, "hr_lam": 1.8, "err_lam": 0.3, "win_boost": 0.25},
    "대구 라이온스": {"hit_lam": 10.5, "hr_lam": 1.2, "err_lam": 0.5, "win_boost": 0.10},
    "부산 이글스": {"hit_lam": 7.5, "hr_lam": 0.7, "err_lam": 0.8, "win_boost": -0.10},
    "인천 호크스": {"hit_lam": 5.0, "hr_lam": 0.4, "err_lam": 1.2, "win_boost": -0.25},
}

# 2. 기본 지표 생성 (포이송 결과는 원래 정수형)
hits = np.array([np.random.poisson(team_stats[t]["hit_lam"]) for t in teams], dtype=int)
home_runs = np.array([np.random.poisson(team_stats[t]["hr_lam"]) for t in teams], dtype=int)
errors = np.array([np.random.poisson(team_stats[t]["err_lam"]) for t in teams], dtype=int)
allowed_hits = np.random.poisson(lam=8.2, size=n_rows).astype(int)

# 3. 낸 점수 / 먹힌 점수 비례 모델링
scored_lam = np.maximum(0.5, hits * 0.42 + home_runs * 1.3)
runs_scored = np.random.poisson(scored_lam).astype(int)

allowed_lam = np.maximum(0.5, (allowed_hits + errors) * 0.45)
runs_allowed = np.random.poisson(allowed_lam).astype(int)

# 4. 득실차 + 팀 부스트 기반 승패(is_win) 확률 연동
score_diff = runs_scored - runs_allowed
base_win_prob = 1 / (1 + np.exp(-score_diff * 0.7))
team_boost = np.array([team_stats[t]["win_boost"] for t in teams])
final_win_prob = np.clip(base_win_prob + team_boost * 0.25, 0.05, 0.95)
is_win = np.random.binomial(1, final_win_prob).astype(int)

df = pd.DataFrame({
    "game_date": dates,
    "team": teams,
    "hits": hits.astype(float),  # 결측치 주입을 위해 float 변환 후 나중에 Nullable Int 적용
    "allowed_hits": allowed_hits,
    "home_runs": home_runs,
    "errors": errors.astype(float),
    "runs_scored": runs_scored,
    "runs_allowed": runs_allowed,
    "is_win": is_win,
})

# [필수] 결측치 주입 (약 5%)
for col in ["hits", "errors"]:
    mask = np.random.rand(n_rows) < 0.05
    df.loc[mask, col] = np.nan

# [필수] 비즈니스 이상치 주입
df.loc[12, "hits"] = 34  
df.loc[12, "runs_scored"] = 19  
df.loc[12, "allowed_scored"] = 19  
df.loc[105, "errors"] = 10  

# [정수형 변환] 결측치 허용 정수형(Int64) 및 일반 정수형(int64) 적용
int_nullable_cols = ["hits", "errors"]
int_strict_cols = ["allowed_hits", "home_runs", "runs_scored", "runs_allowed", "is_win"]

for col in int_nullable_cols:
    df[col] = df[col].astype("Int64")

for col in int_strict_cols:
    df[col] = df[col].astype(int)

# CSV 저장
output_path = "business_data.csv"
df.to_csv(output_path, index=False, encoding="utf-8-sig")
print(f"✅ 데이터 생성 완료 및 저장됨: {output_path}")
print("\n[데이터 타입 확인]\n", df.dtypes)
print("\n[팀별 평균 요약(결측치 제외)]\n", df.groupby('team', observed=True)[['hits', 'home_runs', 'errors', 'runs_scored', 'runs_allowed', 'is_win']].mean())