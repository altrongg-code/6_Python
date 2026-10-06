import matplotlib

matplotlib.use('Agg')

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from config import path, ENCODING
from chart_config import setup, out

setup()


print("=" * 60)
print("1.pandas를 사용하여 train.csv 파일 데이터를 불러와 DataFrame 으로 저장하시오.")

df = pd.read_csv(path('train.csv'), encoding=ENCODING)

print()
print("=" * 60)
print("2. 저장된 데이터에서 상위 5개 행을 출력하시오.")

print(df.head(5))

print()
print("=" * 60)
print("3. 각 열의 이름, 결측치 여부, 데이터 타입(dtype)을 한 번에 확인하시오.")

df.info()

print(df.isna().sum())

print()
print("=" * 60)
print("4. Age(나이), Fare(요금) 열의 평균값, 최솟값, 최댓값을 구하시오.")
age_fare = ['Age', 'Fare']

for c in age_fare:
    print(f"{c} - 평균 : {df[c].mean().round(2)}, 최대 : {df[c].max().round(2)}, 최소 : {df[c].min()}")

print()
print("=" * 60)
print("5. 탑승객 중 생존자와 사망자가 각각 몇 명인지 계산하시오.")

print(f"생존자 : {(df['Survived']==1).sum()}, 사망자 : {(df['Survived']==0).sum()}")

print()
print("=" * 60)
print("6. 객실 등급(Pclass)별로 탑승객이 몇 명인지 계산하시오.")

for p in df['Pclass'].unique().tolist():
    print(f"객실별 탑승객 - {p} 클래스 : {(df['Pclass'] == p).sum()}명")

print()
print("=" * 60)
print("7. 나이가 50세 이상인 탑승객만 추출하여 새로운 데이터프레임을 만드시오.")

new_df = df[df['Age'] >= 50].reset_index(drop=True)

print()
print("=" * 60)
print("8. 탑승객을 나이대 기준으로 그룹화하여 새로운 열 AgeGroup을 추가한 후, 상위 5개 행을 확인하시오.")

bins = [-1, 9, 19, 29, 39, 49, 59, np.inf]
labels = ['아동', '10대', '20대', '30대', '40대', '50대', '60대 이상']

df['AgeGroup'] = pd.cut(df['Age'], bins=bins, labels=labels)
df['AgeGroup'] = df['AgeGroup'].astype(str).replace('nan', '미확인')

print(df[['Age', 'AgeGroup']].head(5))

print()
print("=" * 60)
print("9. 성별(Sex)과 객실 등급(Pclass)을 기준으로 그룹화하여 각각의 평균 생존율을 계산하시오.")

print(df.groupby(['Sex', 'Pclass'])['Survived'].mean().round(2))

print()
print("=" * 60)
print("10. 나이대별 평균 생존율을 계산하시오.")

print(df.groupby(['AgeGroup'])['Survived'].mean().round(2))

print()
print("=" * 60)
print("11. 각 열에 존재하는 결측치(NaN)의 총 개수와 전체 데이터 대비 비율을 계산하여 내림차순으로 출력하시오.")

missing_df = pd.DataFrame({
    'number_of_NaN': df.isna().sum(),
    'rate': (df.isna().sum() / len(df)).round(2)
})
print(missing_df.sort_values(by='number_of_NaN', ascending=False))

print()
print("=" * 60)
print("12. Sex열의 'male'은 0으로, 'female'은 1로 변경하여 Gender_Encoded라는 새로운 열을 추가하시오.")

def gender_encode(s):
    if s == 'male':
        return 0
    elif s == 'female':
        return 1
    else:
        return np.nan
df['Gender_Encoded'] = df['Sex'].apply(gender_encode)
print(df[['Gender_Encoded', 'Sex']].head())

# 딕셔너리로 매핑 정보를 주고 .map()을 호출합니다.
# df['Gender_Encoded'] = df['Sex'].map({'male': 0, 'female': 1})

print()
print("=" * 60)
print("13. 탑승지(Embarked)별로 승객이 지불한 요금(Fare)의 평균을 계산하시오.")

print(df.groupby('Embarked')['Fare'].mean().round(2))

print()
print("=" * 60)
print("14. Pclass를 인덱스로, Sex를 컬럼으로, 값으로 Fare의 평균을 사용하여 피벗 테이블을 생성하시오.")

print(pd.pivot_table(df, 'Fare', 'Pclass', 'Sex'))

print()
print("=" * 60)
print("15. SibSp (형제/배우자 수)와 Parch (부모/자녀 수)를 합산하여 FamilySize 열을 추가하고, 이 열의 요약 통계를 확인하세요.")

df['FamilySize'] = df['SibSp'] + df['Parch']

# FamilySize 열의 요약 통계 확인
print(df['FamilySize'].describe())

print()
print("=" * 60)
print("16. Name 열에서 호칭(Mr., Mrs., Miss., Master. 등)을 정규 표현식 또는 문자열 함수를 사용하여")
print("추출하고 Title이라는 새로운 열을 생성한 뒤, 가장 흔한 5개의 호칭을 출력하시오.")

df['Title'] = df['Name'].str.extract(' ([A-Za-z]+)\.', expand=False)

print(df['Title'].value_counts().head(5))


print()
print("=" * 60)
print("17. 16번에서 생성한 Title 열을 기준으로 그룹화하여, 각 호칭별 승객 수, 평균 나이, 평균 생존율을 한 번에 계산하시오.")

result_df = df.groupby('Title').agg(
    승객수=('PassengerId', 'count'), 
    평균나이=('Age', 'mean'),        
    평균생존율=('Survived', 'mean')   
).round(2)

print(result_df)

print()
print("=" * 60)
print("18. 생존한 사람과 사망한 사람의 나이(Age) 분포를 비교할 수 있도록 시각화하시오.")

fig, ax = plt.subplots(figsize=(11, 5))

df['Survival_Status'] = df['Survived'].map({0: '사망', 1: '생존'})

sns.kdeplot(
    data=df, 
    x='Age', 
    hue='Survival_Status', 
    fill=True, 
    common_norm=False, 
    alpha=0.4, 
    palette={'사망': 'indianred', '생존': 'steelblue'},
    ax=ax
)

ax.set_title('생존 여부에 따른 나이(Age) 분포 비교', fontsize=14, pad=15)
ax.set_xlabel('나이 (Age)')
ax.set_ylabel('밀도 (Density)')

if ax.get_legend():
    ax.get_legend().set_title('생존 여부')

fig.tight_layout()
fig.savefig(out('18_age_distribution.png'), dpi=120)
plt.close(fig)

print()
print("=" * 60)
print("19. 16번에서 추출한 Title과 Pclass를 동시에 고려하여 ")
print("해당 그룹의 나이 중앙값으로 Age 열의 결측치를 대치하시오. (원본 프레임에 적용)")

df['Age'] = df['Age'].fillna(df.groupby(['Title', 'Pclass'])['Age'].transform('median'))

print(f"대치 후 Age 결측치 개수: {df['Age'].isna().sum()}개")

print()
print("=" * 60)
print("20. `Survived`, `Pclass`, `Age`, `SibSp`, `Parch`, `Fare` 등의 수치형 변수들 간의 상관관계 행렬을 계산하고, ")
print("  그 결과를 히트맵(Heatmap) 으로 시각화하시오.")

target_cols = ['Survived', 'Pclass', 'Age', 'SibSp', 'Parch', 'Fare']
corr = df[target_cols].corr()

fig, ax = plt.subplots(figsize=(10, 8))

sns.heatmap(
    corr, 
    annot=True,        
    fmt='.2f',         
    cmap='coolwarm',   
    center=0,          
    linewidths=0.5,    
    xticklabels=target_cols,
    yticklabels=target_cols,
    cbar_kws={'label': '상관계수'},
    ax=ax
)

ax.set_xticklabels(ax.get_xticklabels(), rotation=0, ha='center', fontsize=11)
ax.set_yticklabels(ax.get_yticklabels(), rotation=0, va='center', fontsize=11)

ax.set_title('수치형 변수들 간의 상관', fontsize=14, pad=15)

fig.tight_layout()
fig.savefig(out('20_corr_heatmap.png'), dpi=120, bbox_inches='tight')
plt.close(fig)



