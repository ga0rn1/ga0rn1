# app.py

import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------
# 데이터 로드
# -----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("countriesMBTI_16types.csv")
    return df

df = load_data()

# -----------------------------
# Streamlit 앱 UI
# -----------------------------
st.title("🌍 국가별 MBTI 유형 분포 시각화")
st.markdown("국가를 선택하면 해당 나라의 MBTI 16유형 분포를 인터랙티브 막대그래프로 볼 수 있습니다.")

# -----------------------------
# 국가 선택 위젯
# -----------------------------
selected_country = st.selectbox("국가를 선택하세요:", df['Country'].unique())

# -----------------------------
# 선택한 국가 데이터 필터링
# -----------------------------
country_data = df[df['Country'] == selected_country].iloc[0, 1:]  # Country 제외

# -----------------------------
# 막대그래프 데이터프레임 변환
# -----------------------------
bar_df = pd.DataFrame({
    'MBTI Type': country_data.index,
    'Percentage': country_data.values
}).sort_values(by='Percentage', ascending=False)

# -----------------------------
# 색상 설정 (1등은 빨강, 나머지는 파랑 그라데이션)
# -----------------------------
colors = ['#FF4B4B'] + px.colors.sequential.Blues_r[2:len(bar_df)]

# -----------------------------
# Plotly 막대 그래프 생성
# -----------------------------
fig = px.bar(
    bar_df,
    x='MBTI Type',
    y='Percentage',
    title=f"{selected_country}의 MBTI 분포",
    text='Percentage',
    color_discrete_sequence=colors
)

fig.update_traces(
    texttemplate='%{text:.2%}',
    textposition='outside',
    hovertemplate='<b>%{x}</b><br>비율: %{y:.2%}'
)

fig.update_layout(
    xaxis_title="MBTI 유형",
    yaxis_title="비율",
    uniformtext_minsize=8,
    uniformtext_mode='hide',
    plot_bgcolor='white',
    title_x=0.5,
)

# -----------------------------
# 그래프 출력
# -----------------------------
st.plotly_chart(fig, use_container_width=True)

# ============================================================
# 추가 기능: MBTI 유형별로 국가 순위 그래프
# ============================================================
st.markdown("---")
st.subheader("🌐 MBTI 유형별 국가 순위 비교")
st.markdown("특정 MBTI 유형을 선택하면, 해당 유형 비율이 높은 국가 순으로 막대 그래프가 표시됩니다.")

# MBTI 유형 선택
selected_type = st.selectbox("MBTI 유형을 선택하세요:", [c for c in df.columns if c != 'Country'])

# 해당 유형별 국가 순위 계산
rank_df = df[['Country', selected_type]].sort_values(by=selected_type, ascending=False).reset_index(drop=True)

# 색상 설정 (1등은 노랑, 나머지는 회색, 한국은 파랑)
colors = []
for i, row in rank_df.iterrows():
    if row['Country'].lower() in ['south korea', 'korea', 'republic of korea', '대한민국']:
        colors.append('#007BFF')  # 파랑
    elif i == 0:
        colors.append('#FFD700')  # 노랑
    else:
        colors.append('#C0C0C0')  # 회색

# 그래프 생성
fig2 = px.bar(
    rank_df,
    x='Country',
    y=selected_type,
    title=f"{selected_type} 유형 비율이 높은 국가 순위",
    text=selected_type
)

fig2.update_traces(
    marker_color=colors,
    texttemplate='%{text:.2%}',
    textposition='outside',
    hovertemplate='<b>%{x}</b><br>비율: %{y:.2%}'
)

fig2.update_layout(
    xaxis_title="국가",
    yaxis_title="비율",
    plot_bgcolor='white',
    title_x=0.5,
)

st.plotly_chart(fig2, use_container_width=True)
