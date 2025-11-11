import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------
# 필수 패키지 설치 안내
# -----------------------------
st.markdown("""
### 📦 Requirements (requirements.txt)
```
streamlit
plotly
pandas
```
""")

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

# -----------------------------
# 코드 복사 안내
# -----------------------------
st.markdown("""
---
📋 **복사 안내:** 위 코드를 전체 복사하여 Streamlit Cloud에 업로드하면 작동합니다.
- 파일명: `app.py`
- CSV 파일: `countriesMBTI_16types.csv`
- requirements.txt 위 내용 복사
""")
