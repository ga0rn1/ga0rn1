import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np

# ================================
# 데이터 불러오기
# ================================
@st.cache_data
def load_data():
    # Streamlit Cloud에서 pages/ 폴더 기준이기 때문에 ../subway.csv 경로 사용
    return pd.read_csv("../subway.csv", encoding="cp949")

df = load_data()

st.title("🚇 2025년 10월 지하철 승하차 분석")
st.write("날짜와 호선을 선택하면 승하차 총합이 높은 역 순으로 막대그래프를 확인할 수 있어요.")

# ================================
# 날짜 / 호선 선택 UI
# ================================
df["사용일자"] = df["사용일자"].astype(str)

df_oct = df[df["사용일자"].str.startswith("202510")]

date_list = sorted(df_oct["사용일자"].unique())
line_l_

