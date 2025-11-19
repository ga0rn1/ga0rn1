# pages/blood_type_analysis.py
import streamlit as st
import pandas as pd
import plotly.express as px
import os

# 페이지 설정
st.set_page_config(layout="wide")
st.title("📈 혈액형 순위 분석 (전체 검사 인원 기준)")
st.caption("🚨 참고: '2025년 인구'는 CSV 파일에 기록된 전체 지역의 '검사인원' 합계를 기준으로 가정했습니다.")

@st.cache_data
def load_data():
    """상위 폴더에 있는 abc.csv 파일을 로드합니다."""
    # pages 폴더 내의 코드에서 상위 폴더의 파일에 접근
    file_path = os.path.join(os.path.dirname(__file__), '..', 'abc.csv')
    try:
        df = pd.read_csv(file_path)
        return df
    except FileNotFoundError:
        st.error(f"오류: 파일을 찾을 수 없습니다. 경로를 확인해 주세요: {file_path}")
        return pd.DataFrame()

def create_blood_type_chart(df):
    """
    Rh+ 혈액형 (A, B, O, AB)의 전체 합계를 기준으로 순위를 계산하고
    Plotly 막대 그래프를 생성합니다.
    """
    if df.empty:
        return None

    # 1. Rh+형 혈액형의 전체 합계 계산 및 순위 결정
    blood_types_cols = ['A형', 'B형', 'O형', 'AB형']
    # 전체 인구 대신 전체 검사 인원을 혈액형별로 합산
    total_counts = df[blood_types_cols].sum().sort_values(ascending=False)

    # 2. Plotly용 DataFrame 생성
    plot_df = total_counts.reset_index()
    plot_df.columns = ['혈액형', '총 검사 인원 (명)']

    # 3. 색상 설정 (1등: 빨강, 나머지: 파란색 그라데이션)
    # 1등을 찾고, 그 순서에 따라 색상 매핑을 정의합니다.
    color_map = {}
    
    # 1등: 빨강 (#E74C3C)
    color_map[plot_df.iloc[0]['혈액형']] = '#E74C3C' 
    
    # 나머지 (2, 3, 4등): 파란색 그라데이션 (어두운 파랑 -> 중간 파랑 -> 밝은 파랑 순)
    blue_gradient_colors = ['#3498DB', '#85C1E9', '#AED6F1'] 
    for i in range(1, len(plot_df)):
        if i-1 < len(blue_gradient_colors):
            color_map[plot_df.iloc[i]['혈액형']] = blue_gradient_colors[i-1]
        else:
             # 안전 장치 (혹시 4개 이상의 혈액형이 있을 경우)
             color_map[plot_df.iloc[i]['혈액형']] = '#AED6F1'

    # 4. Plotly Bar Chart 생성
    fig = px.bar(
        plot_df,
        x='혈액형',
        y='총 검사 인원 (명)',
        color='혈액형', # '혈액형' 컬럼을 기준으로 색상을 구분
        color_discrete_map=color_map, # 커스텀 색상 맵 적용
        title="2025년 (가정) 혈액형별 총 인원 순위",
        text='총 검사 인원 (명)'
    )

    # 5. 차트 레이아웃 및 스타일 설정
    fig.update_traces(
        texttemplate='%{text:,.0f}명', # 텍스트 포맷 (천단위 구분 기호 추가)
        textposition='outside' # 막대 바깥에 표시
    )
    
    fig.update_layout(
        xaxis_title='혈액형',
        yaxis_title='총 검사 인원 (명)',
        font=dict(size=14),
        showlegend=False, # 범례 숨김
        # 제목 중앙 정렬
        title_x=0.5
    )

    # y축을 0에서 시작하도록 설정
    fig.update_yaxes(rangemode="tozero", tickformat=",") 
    
    return fig, plot_df

# 메인 실행 로직
df = load_data()

if not df.empty:
    chart_fig, plot_df_results = create_blood_type_chart(df)
    
    if chart_fig:
        # 1. Plotly 인터랙티브 그래프 출력
        st.plotly_chart(chart_fig, use_container_width=True)
        
        st.divider()

        # 2. 분석 결과 테이블 출력
        st.subheader("📊 분석 결과 (순위표)")
        # 순위 컬럼 추가
        plot_df_results.insert(0, '순위', range(1, 1 + len(plot_df_results)))
        # 숫자 컬럼 포맷팅
        styled_df = plot_df_results.style.format({'총 검사 인원 (명)': "{:,.0f}"})
        st.dataframe(styled_df, hide_index=True)
