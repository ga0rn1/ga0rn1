import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# -----------------------------
# 데이터 불러오기
# -----------------------------
@st.cache_data
def load_data():
    return pd.read_csv("../subway.csv", encoding="cp949")

df = load_data()

st.title("🚇 지하철 승하차 분석 (2025년 10월)") 
st.write("날짜와 호선을 선택하면, 승하차 총합이 높은 역 순으로 시각화합니다.")

# -----------------------------
# 날짜 & 호선 선택
# -----------------------------
df["사용일자"] = df["사용일자"].astype(str)

# 2025년 10월만 필터링
df_oct = df[df["사용일자"].str.startswith("202510")]

date_list = sorted(df_oct["사용일자"].unique())
line_list = sorted(df_oct["노선명"].unique())

selected_date = st.selectbox("📅 날짜 선택", date_list)
selected_line = st.selectbox("🚇 호선 선택", line_list)

# -----------------------------
# 선택한 조건으로 필터링
# -----------------------------
filtered = df_oct[
    (df_oct["사용일자"] == selected_date) &
    (df_oct["노선명"] == selected_line)
].copy()

if filtered.empty:
    st.warning("데이터가 없습니다.")
    st.stop()

# -----------------------------
# 승하차 총합 계산
# -----------------------------
filtered["총승하차"] = filtered["승차총승객수"] + filtered["하차총승객수"]
filtered = filtered.sort_values("총승하차", ascending=False)

# -----------------------------
# 색상 처리 (1등=빨강, 나머지=파랑→흐려지는 그라데이션)
# -----------------------------
color_list = ["red"]  # 1등 빨강

if len(filtered) > 1:
    blue_shades = [
        f"rgba(0, 0, 255, {opacity})"
        for opacity in list(
            reversed([i / (len(filtered) - 1) for i in range(1, len(filtered))])
        )
    ]
    color_list.extend(blue_shades)

# -----------------------------
# Plotly 막대그래프 생성
# -----------------------------
fig = go.Figure()

fig.add_trace(
    go.Bar(
        x=filtered["역명"],
        y=filtered["총승하차"],
        marker=dict(color=color_list),
        text=filtered["총승하차"],
        textposition='outside'
    )
)

fig.update_layout(
    title=f"{selected_date} · {selected_line} 승하차 TOP 역",
    xaxis_title="역명",
    yaxis_title="총 승하차 인원",
    template="simple_white",
    height=600,
)

st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# Raw Data 확인용
# -----------------------------
with st.expander("📄 데이터 보기"):
    st.dataframe(filtered.reset_index(drop=True))
