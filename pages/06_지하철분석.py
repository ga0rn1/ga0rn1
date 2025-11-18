import streamlit as st
import pandas as pd
import plotly.graph_graphql as go

# ================================
# CSV 로드
# ================================
@st.cache_data
def load_data():
    try:
        return pd.read_csv("../subway.csv", encoding="cp949")
    except:
        return pd.read_csv("../subway.csv", encoding="utf-8")


df = load_data()

st.title("🚇 2025년 10월 지하철 승하차 분석")
st.write("날짜와 호선을 선택하면 승하차 총합이 높은 역순으로 그래프가 표시됩니다.")

# 날짜를 문자열 처리
df["사용일자"] = df["사용일자"].astype(str)

# 2025년 10월 데이터만 사용
df_oct = df[df["사용일자"].str.startswith("202510")]

# UI 선택창
date_list = sorted(df_oct["사용일자"].unique())
line_list = sorted(df_oct["노선명"].unique())

selected_date = st.selectbox("📅 날짜 선택", date_list)
selected_line = st.selectbox("🚇 호선 선택", line_list)

# 필터링
filtered = df_oct[
    (df_oct["사용일자"] == selected_date) &
    (df_oct["노선명"] == selected_line)
].copy()

if filtered.empty:
    st.error("해당 조건의 데이터가 없습니다.")
    st.stop()

# 승하차 합계
filtered["총승하차"] = filtered["승차총승객수"] + filtered["하차총승객수"]
filtered = filtered.sort_values("총승하차", ascending=False).reset_index(drop=True)

# ================================
# 색상: 1등 빨강, 나머지 파랑 → 투명해짐
# ================================
colors = []
for i in range(len(filtered)):
    if i == 0:
        colors.append("rgba(255,0,0,1)")  # 1등 빨강
    else:
        opacity = max(0.15, 1 - (i / (len(filtered) + 1)))  # 완전 투명해지는 것 방지
        colors.append(f"rgba(0, 0, 255, {opacity})")

# ================================
# Plotly 그래프
# ================================
fig = go.Figure()

fig.add_trace(
    go.Bar(
        x=filtered["역명"],
        y=filtered["총승하차"],
        marker=dict(color=colors),
        text=[f"{int(x):,}" for x in filtered["총승하차"]],
        textposition="outside"
    )
)

fig.update_layout(
    title=f"{selected_date} | {selected_line} 승하차 총합 순위",
    xaxis_title="역명",
    yaxis_title="총 승하차 인원",
    template="simple_white",
    height=600,
    margin=dict(l=30, r=30, t=70, b=120)
)

st.plotly_chart(fig, use_container_width=True)

# ================================
# 데이터 확인
# ================================
with st.expander("📄 필터링된 데이터 보기"):
    st.dataframe(filtered)
