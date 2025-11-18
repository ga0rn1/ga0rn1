import streamlit as st
import pandas as pd
import plotly.graph_objects as go

@st.cache_data
def load_data():
    try:
        return pd.read_csv("../subway.csv", encoding="cp949")
    except:
        return pd.read_csv("../subway.csv", encoding="utf-8")

df = load_data()

df["사용일자"] = df["사용일자"].astype(str)
df_oct = df[df["사용일자"].str.startswith("202510")]

st.title("지하철 승하차 분석")

date_list = sorted(df_oct["사용일자"].unique())
line_list = sorted(df_oct["노선명"].unique())

selected_date = st.selectbox("날짜 선택", date_list)
selected_line = st.selectbox("호선 선택", line_list)

filtered = df_oct[
    (df_oct["사용일자"] == selected_date) &
    (df_oct["노선명"] == selected_line)
].copy()

if filtered.empty:
    st.write("데이터 없음")
    st.stop()

filtered["총승하차"] = filtered["승차총승객수"] + filtered["하차총승객수"]
filtered = filtered.sort_values("총승하차", ascending=False).reset_index(drop=True)

colors = []
for i in range(len(filtered)):
    if i == 0:

