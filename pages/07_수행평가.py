import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np

st.set_page_config(page_title="Device Usage Analysis", layout="wide")

# CSV 파일 로드 (앱 최상위 폴더에서 읽기)
@st.cache_data
def load_data():
    return pd.read_csv("user_behavior_dataset.csv")

df = load_data()

st.title("📱 Device Model Usage Analysis")
st.write("기기별 하루 평균 앱 사용시간을 기준으로 정렬한 인터랙티브 라인 그래프입니다.")

# 1) 기기별 평균 사용시간 계산
device_usage = (
    df.groupby("Device Model")["App Usage Time (min/day)"]
    .mean()
    .sort_values(ascending=False)
)

st.subheader("기기별 평균 사용시간 순위")
st.dataframe(device_usage.reset_index(), use_container_width=True)

# 2) 그래프 색상 설정
colors = []

# 1등 빨간색
colors.append("red")

# 주황 → 밝은 주황 그라데이션
base_color = np.array([255, 165, 0])   # Orange (RGB)
steps = len(device_usage) - 1

for i in range(steps):
    factor = 0.85 + (i / steps) * 0.15  # 실질적으로 밝기 변화
    new_color = (base_color * factor).astype(int)
    colors.append(f"rgb({new_color[0]}, {new_color[1]}, {new_color[2]})")

# 3) Plotly Line Chart
fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=device_usage.index,
        y=device_usage.values,
        mode="lines+markers",
        line=dict(width=3),
        marker=dict(size=10, color=colors),
        text=[f"{v:.1f} min/day" for v in device_usage.values],
        hovertemplate="%{x}<br>사용시간: %{y} min/day"
    )
)

fig.update_layout(
    title="📈 기기별 하루 평균 앱 사용 시간 (정렬)",
    xaxis_title="Device Model",
    yaxis_title="App Usage Time (min/day)",
    xaxis_tickangle=-45,
    template="plotly_white",
    height=600,
)

st.plotly_chart(fig, use_container_width=True)
