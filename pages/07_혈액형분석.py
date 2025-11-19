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
    """상위 폴더에 있는 abc.csv 파일을 가장 강력한 방식으로 로드합니다."""
    
    # 💡 파일 경로 설정: 'pages' 폴더에서 상위 폴더('../')의 'abc.csv'에 접근
    file_path = os.path.join(os.path.dirname(__file__), '..', 'abc.csv')
    encodings_to_try = ['utf-8', 'utf-8-sig', 'cp949', 'euc-kr']
    
    # 1. 파일 존재 여부 확인 (경로 문제 확인)
    if not os.path.exists(file_path):
        st.error(f"🚨 파일 경로 오류: 'abc.csv' 파일을 찾을 수 없습니다. 파일을 **'pages' 폴더의 상위 폴더**에 배치했는지 확인해 주세요.")
        return pd.DataFrame()

    # 2. 인코딩 순차 시도 (디코딩 문제 해결)
    for encoding in encodings_to_try:
        try:
            # 가장 흔한 4가지 인코딩 순차 시도
            df = pd.read_csv(file_path, encoding=encoding) 
            
            # 데이터 로드 성공 확인 (정상적인 데이터가 맞는지 확인하는 간단한 검증)
            if '검사인원' in df.columns and len(df) > 0:
                st.success(f"✅ CSV 파일을 '{encoding}' 인코딩으로 성공적으로 로드했습니다.")
                return df
            else:
                # 파일은 읽었으나 내용이 이상할 경우 (예: 헤더만 있고 데이터 없음)
                st.warning(f"경고: '{encoding}'으로 로드되었으나, 데이터 내용이 비어있거나 예상 컬럼('검사인원' 등)이 없습니다.")
                continue 
        except UnicodeDecodeError:
            # 해당 인코딩으로 읽기 실패 시 다음 인코딩 시도
            continue
        except Exception as e:
            # 기타 예외 (CSV 파싱 오류 등)
            st.warning(f"경고 ({encoding} 시도 중): 기타 오류 발생. 다음 인코딩을 시도합니다. (오류: {e})")
            continue

    # 모든 인코딩 시도 실패
    st.error("❌ 치명적 오류: 파일을 찾았으나, 모든 일반적인 인코딩(utf-8, utf-8-sig, cp949, euc-kr)으로 읽을 수 없습니다. 파일의 인코딩을 확인하거나, 텍스트 편집기로 열어 내용을 확인해 보세요.")
    return pd.DataFrame()

def create_blood_type_chart(df):
    """
    Rh+ 혈액형 (A, B, O, AB)의 전체 합계를 기준으로 순위를 계산하고
    Plotly 막대 그래프를 생성합니다.
    """
    if df.empty:
        st.stop() # 데이터가 없으면 실행 중지

    # 1. Rh+형 혈액형의 전체 합계 계산 및 순위 결정
    # 주의: CSV 메타데이터를 보니 'A형', 'B형', 'O형', 'AB형' 컬럼이 있는 것으로 판단됩니다.
    blood_types_cols = ['A형', 'B형', 'O형', 'AB형']
    
    # 필요한 컬럼이 데이터프레임에 있는지 최종 확인
    if not all(col in df.columns for col in blood_types_cols):
        st.error("🚨 컬럼 오류: 필수 혈액형 컬럼('A형', 'B형', 'O형', 'AB형') 중 일부를 찾을 수 없습니다. CSV 파일의 컬럼명을 확인해 주세요.")
        st.dataframe(df.head()) # 로드된 데이터의 상위 5행 보여주기
        st.stop()
        
    # 전체 인구 대신 전체 검사 인원을 혈액형별로 합산
    # .sum(numeric_only=True)를 사용하여 숫자만 합산하도록 보장
    total_counts = df[blood_types_cols].sum(numeric_only=True).sort_values(ascending=False)

    # 2. Plotly용 DataFrame 생성
    plot_df = total_counts.reset_index()
    plot_df.columns = ['혈액형', '총 검사 인원 (명)']

    # 3. 색상 설정 (1등: 빨강, 나머지: 파란색 그라데이션)
    color_map = {}
    
    # 1등: 빨강 (#E74C3C)
    color_map[plot_df.iloc[0]['혈액형']] = '#E74C3C' 
    
    # 나머지 (2, 3, 4등): 파란색 그라데이션 
    # (2등: #3498DB, 3등: #85C1E9, 4등: #AED6F1)
    blue_gradient_colors = ['#3498DB', '#85C1E9', '#AED6F1'] 
    for i in range(1, len(plot_df)):
        if i - 1 < len(blue_gradient_colors):
            color_map[plot_df.iloc[i]['혈액형']] = blue_gradient_colors[i-1]
        else:
             color_map[plot_df.iloc[i]['혈액형']] = '#AED6F1'

    # 4. Plotly Bar Chart 생성
    fig = px.bar(
        plot_df,
        x='혈액형',
        y='총 검사 인원 (명)',
        color='혈액형',
        color_discrete_map=color_map,
        title="2025년 (가정) 혈액형별 총 인원 순위",
        text='총 검사 인원 (명)'
    )

    # 5. 차트 레이아웃 및 스타일 설정
    fig.update_traces(
        texttemplate='%{text:,.0f}명',
        textposition='outside'
    )
    
    fig.update_layout(
        xaxis_title='혈액형',
        yaxis_title='총 검사 인원 (명)',
        font=dict(size=14),
        showlegend=False,
        title_x=0.5
    )
    fig.update_yaxes(rangemode="tozero", tickformat=",") 
    
    return fig, plot_df

# 메인 실행 로직
df = load_data()

# 데이터 로드에 성공했을 때만 차트 생성 및 표시
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
        st.dataframe(styled_df, hide_index=True, use_container_width=True)
    
