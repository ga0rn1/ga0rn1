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
        # 💡 수정된 부분: 인코딩 옵션 추가 (대부분의 한글 CSV 파일은 'cp949' 또는 'euc-kr'입니다.)
        df = pd.read_csv(file_path, encoding='cp949') 
        return df
    except FileNotFoundError:
        st.error(f"오류: 파일을 찾을 수 없습니다. 경로를 확인해 주세요: {file_path}")
        return pd.DataFrame()
    except UnicodeDecodeError:
        # cp949로도 실패하면 utf-8-sig나 euc-kr 등을 시도할 수 있습니다.
        try:
            df = pd.read_csv(file_path, encoding='euc-kr')
            return df
        except:
             st.error("오류: CSV 파일을 'cp949' 또는 'euc-kr' 인코딩으로 읽을 수 없습니다. 파일 인코딩을 확인해 주세요.")
             return pd.DataFrame()

# ... (나머지 코드는 동일)
