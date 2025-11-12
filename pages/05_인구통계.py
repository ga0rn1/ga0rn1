import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="인구 연령대 시각화", layout="centered")

st.title("📊 2025년 10월 기준 행정구역별 연령대 인구 시각화")

# -------------------------------
# ✅ 데이터 불러오기 및 정제
# -------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("population.csv")

    # 숫자형으로 변환 (쉼표 제거)
    numeric_cols = [col for col in df.columns if "계_" in col and "~" in col]
    for col in numeric_cols:
        df[col] = (
            df[col]
            .astype(str)
            .str.replace(",", "", regex=False)
            .str.replace("-", "0", regex=False)
            .astype(float)
        )
    return df, numeric_cols

df, numeric_cols = load_data()

# -------------------------------
# ✅ 행정구 선택
# -------------------------------
regions = df["행정구역"].unique()
selected_region = st.selectbox("행정구역을 선택하세요 👇", regions)

# -------------------------------
# ✅ 선택한 지역의 연령대 인구 추출
# -------------------------------
row = df[df["행정구역"] == selected_region].iloc[0]
ages = [col.split("_")[-1] for col in numeric_cols]
values = [row[col] for col in numeric_cols]

# -------------------------------
# ✅ 그래프 생성
# -------------------------------
fig, ax = plt.subplots(figsize=(10, 5))
fig.patch.set_facecolor("#e6e6e6")  # 회색 바탕

ax.plot(ages, values, color="black", marker="o", linewidth=2)

ax.set_title(f"{selected_region} 연령대별 인구 분포", fontsize=15, pad=15)
ax.set_xlabel("연령대", fontsize=12)
ax.set_ylabel("인구수", fontsize=12)

# X축 설정 (10살 단위)
ax.set_xticks(range(len(ages)))
ax.set_xticklabels(ages, rotation=45)

# Y축 설정 (100명 단위)
max_y = int(max(values))
step = 100
ax.set_yticks(range(0, max_y + step, step))

# 보조선 및 배경
ax.grid(True, linestyle="--", alpha=0.5)

st.pyplot(fig)

st.caption("※ 데이터 출처: 2025년 10월 기준 행정구역별 인구 통계")
