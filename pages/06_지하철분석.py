import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os

# ---------------------------
# 데이터 로드
# ---------------------------
@st.cache_data
def load_data():
    # Streamlit Cloud에서는 상대경로 ../ 불안정 → 현재 폴더 기준으로 강제 변경
    fname = "subway.csv"
    if not os.path.exists(fname):  # 혹시 상위 폴더에 있는 경우
        fname = "../subway.csv"

    try:
        return pd.read_csv(fname, encoding="cp949")
    except:
        return pd.read_csv(fname, encoding="utf-8")

df = load_data()

# 날짜 문자열 처리
df["사용일자"] = df["사용일자"].astype(str)
df_oct = df[df["사용일자"].str.startswith("202510")]

# ---------------------------
# UI
# ---------------------------
st.title("지하철 승하차 분석")

date_list = sorted(df_oct["사용일자"].unique())
line_list = sorted(df_oct["노선명"].unique())

selected_date = st.selectbox("날짜 선택", date_list)
selected_line = st.selectbox("호선 선택", line_list)

# ---------------------------
# 데이터 필터링
# ---------------------------
filtered = df_oct[
    (df_oct["사용일자"] == selected_date) &
    (df_oct["노선명"] == selected_line)
].copy()

if filtered.empty:
    st.write("데이터 없음")
    st.stop()

filtered["총승하차"] = filtered["승차총승객수"] + filtered["하차총승객수"]
filtered = filtered.sort_values("총승하차", ascending=False).reset_index(drop=True)

# ---------------------------
# 색상 설정 (1위는 빨강, 나머지 파랑 투명도 변화)
# ---------------------------
colors = []
for i in range(len(filtered)):
    if i == 0:
        colors.append("rgba(255,0,0,1)")
    else:
        opacity = 1 - (i / (len(filtered) + 2))
        colors.append(f"rgba(0,0,255,{opacity})")

# ---------------------------
# 그래프 생성
# ---------------------------
fig = go.Figure()
fig.add_bar(
    x=filtered["역명"],
    y=filtered["총승하차"],
    marker_color=colors
)
fig.update_layout(
    title="승하차 순위",
    xaxis_title="역명",
    yaxis_title="승하차 합계",
    height=600
)

st.plotly_chart(fig, use_container_width=True)
st.dataframe(filtered)
