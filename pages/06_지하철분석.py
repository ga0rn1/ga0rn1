import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# ================================
# 데이터 로드
# ================================
@st.cache_data
def load_data():
    try:
        return pd.read_csv("../subway.csv", encoding="cp949")
    except:
        return pd.read_csv("../subway.csv", encoding="utf-8")

df = load_data()

st.title("🚇 2025년 10월 지하철 승하차 분석")

# 날짜 문자열 처리
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
    (df_oct_
