# pages/06_지하철분석.py
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path
from typing import Optional

st.set_page_config(page_title="지하철 승하차 분석", layout="wide")

@st.cache_data
def robust_read_csv(path: Path) -> pd.DataFrame:
    """
    여러 인코딩/구분자 시도해서 CSV 읽기.
    """
    encodings = ["cp949", "euc-kr", "utf-8", "utf-8-sig"]
    seps = [",", ";", "\t"]
    last_exc: Optional[Exception] = None
    for enc in encodings:
        for sep in seps:
            try:
                df = pd.read_csv(path, encoding=enc, sep=sep)
                return df
            except Exception as e:
                last_exc = e
    # 마지막 예외 다시 던지기
    raise last_exc

def normalize_date_col(df: pd.DataFrame, col: str = "사용일자") -> pd.DataFrame:
    # 컬럼 이름 양쪽 공백 제거(혹시 공백 섞여있을 경우)
    df = df.rename(columns=lambda c: c.strip())
    if col not in df.columns:
        raise KeyError(f"'{col}' 컬럼이 없습니다. 파일의 컬럼: {df.columns.tolist()}")
    # 숫자형이면 문자열로, 길이 8이 아니라면 왼쪽 0 채움
    ser = df[col]
    if pd.api.types.is_integer_dtype(ser) or pd.api.types.is_float_dtype(ser):
        ser = ser.astype(int).astype(str)
    else:
        ser = ser.astype(str)
    ser = ser.str.strip()
    # 만약 YYYYMM 또는 YYYYMMDD 등 형태 다양하면 8자리로 맞추기(가능하면)
    ser = ser.apply(lambda s: s.zfill(8) if s.isdigit() and len(s) < 8 else s)
    df[col] = ser
    return df

# 파일 경로: 이 페이지 파일의 상위 폴더에 subway.csv 가 있다고 가정
BASE = Path(__file__).resolve().parents[1]  # pages의 상위 폴더
CSV_PATH = BASE / "subway.csv"

st.title("지하철 승하차 분석 (Plotly 인터랙티브)")

# 파일 존재 체크
if not CSV_PATH.exists():
    st.error(f"CSV 파일을 찾을 수 없습니다: {CSV_PATH}\n(이 페이지 파일은 pages 폴더에 있고, CSV는 그 상위 폴더에 있어야 합니다.)")
    st.stop()

# 데이터 읽기
try:
    df = robust_read_csv(CSV_PATH)
except Exception as e:
    st.error("CSV 파일 로드에 실패했습니다. 자동으로 시도한 인코딩/구분자를 모두 실패했습니다.")
    st.exception(e)
    st.stop()

# 날짜 컬럼 정리
try:
    df = normalize_date_col(df, col="사용일자")
except Exception as e:
    st.error("사용일자 컬럼 처리 중 오류가 발생했습니다.")
    st.exception(e)
    st.stop()

# 컬럼명 공백 제거
df = df.rename(columns=lambda c: c.strip())

# 필요한 칼럼 확인
required_cols = {"사용일자", "노선명", "역명", "승차총승객수", "하차총승객수"}
missing = required_cols - set(df.columns)
if missing:
    st.error(f"필수 컬럼이 누락되었습니다: {missing}")
    st.write("현재 파일의 컬럼들:", df.columns.tolist())
    st.stop()

# 숫자형 변환(승차/하차)
for col in ["승차총승객수", "하차총승객수"]:
    df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0).astype(int)

# 2025년 10월(YYYYMM == 202510) 날짜 목록
available_dates = sorted(df["사용일자"].unique())
oct_2025_dates = [d for d in available_dates if str(d).startswith("202510")]

# UI: 날짜/호선 선택
st.sidebar.header("필터")
if oct_2025_dates:
    selected_date = st.sidebar.selectbox("날짜 선택 (2025년 10월)", oct_2025_dates, index=0)
else:
    st.sidebar.warning("데이터에 2025년 10월(202510) 날짜가 없습니다. 사용 가능한 날짜 중 선택하세요.")
    selected_date = st.sidebar.selectbox("날짜 선택 (available)", available_dates, index=0)

# 호선 목록 (선택된 날짜 기준으로 채움, 비어있으면 전체 호선)
lines_for_date = sorted(df[df["사용일자"] == selected_date]["노선명"].dropna().unique().tolist())
if not lines_for_date:
    # 선택 날짜에 해당 데이터가 없다면 전체 노선 사용
    lines_for_date = sorted(df["노선명"].dropna().unique().tolist())

selected_line = st.sidebar.selectbox("호선 선택", lines_for_date)

# 필터링
filtered = df[(df["사용일자"] == selected_date) & (df["노선명"] == selected_line)].copy()

if filtered.empty:
    st.info("선택한 날짜/호선으로 검색된 데이터가 없습니다. 아래 원본 데이터 예시와 함께 사용 가능한 날짜/호선을 확인하세요.")
    st.subheader("파일에서 읽은 사용 가능한 날짜(최대 20개)")
    st.write(available_dates[:20])
    st.subheader("파일에서 읽은 노선 목록(최대 50개)")
    st.write(sorted(df["노선명"].dropna().unique().tolist()[:50]))
    st.stop()

# 계산 및 정렬
filtered["총승하차"] = filtered["승차총승객수"] + filtered["하차총승객수"]
filtered = filtered.sort_values("총승하차", ascending=False).reset_index(drop=True)

# 색상 생성: 1등 빨강, 나머지 파란색에서 흐려짐
n = len(filtered)
colors = []
for i in range(n):
    if i == 0:
        colors.append("rgba(255,0,0,1)")
    else:
        # opacity 0.95 down to 0.2 (선형)
        min_op = 0.20
        max_op = 0.95
        if n > 1:
            # i from 1..n-1 -> t from 0..1
            t = (i - 1) / max(1, (n - 2))
            opacity = max_op - (max_op - min_op) * t
        else:
            opacity = max_op
        colors.append(f"rgba(0,0,255,{opacity:.3f})")

# 그래프 그리기 (Plotly)
fig = go.Figure()
fig.add_trace(
    go.Bar(
        x=filtered["역명"],
        y=filtered["총승하차"],
        marker=dict(color=colors),
        hovertemplate="<b>%{x}</b><br>총승하차: %{y}<br><extra></extra>"
    )
)
fig.update_layout(
    title=f"{selected_date} - {selected_line} 승하차 합계 (내림차순)",
    xaxis_title="역명",
    yaxis_title="승하차 합계",
    xaxis_tickangle=-45,
    height=650,
    margin=dict(l=40, r=20, t=80, b=160)
)

st.plotly_chart(fig, use_container_width=True)

st.subheader("상세 테이블")
st.dataframe(filtered)
