import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="인구 연령대 시각화", layout="centered")

st.title("📊 2025년 10월 기준 행정구역별 연령대 인구 시각화")

# --- 데이터 불러오기 ---
@st.cache_data
def load_data():
    df = pd.read_csv("population.csv")
    # 숫자형 변환
    num_cols = [col for col in df.columns if "계_" in col and "~" in col]
    for col in num_cols:
        df[col] = df[col].astype(str).str.replace(",", "").astype(int)
    return df

df = load_data()

# --- 행정구 선택 ---
regions = df["행정구역"].unique()
selected_region = st.selectbox("행정구역을 선택하세요:", regions)

# --- 선택한 지역 데이터 필터 ---
row = df[df["행정구역"] == selected_region].iloc[0]

# --- 연령대별 인구 데이터 추출 ---
age_cols = [col for col in df.columns if "계_" in col and "~" in col]
ages = [col.split("_")[-1] for col in age_cols]
values = [row[col] for col in age_cols]

# --- 그래프 그리기 ---
fig, ax = plt.subplots(figsize=(10, 5))
fig.patch.set_facecolor("#f0f0f0")  # 회색 배경
ax.plot(ages, values, color="black", marker="o", linewidth=2)

# 축 설정
ax.set_xlabel("연령대", fontsize=12)
ax.set_ylabel("인구수", fontsize=12)
ax.set_title(f"{selected_region} 연령대별 인구 분포", fontsize=14, pad=15)

# x축: 10살 단위 구분선
ax.set_xticks(ages)
ax.tick_params(axis='x', rotation=45)

# y축: 100명 단위 구분선
max_y = (max(values) // 100 + 1) * 100
ax.set_yticks(range(0, max_y + 100, 100))

ax.grid(True, linestyle="--", alpha=0.5)

st.pyplot(fig)


