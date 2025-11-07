import streamlit as st
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="서울 관광 명소 지도", layout="wide")

st.title("🗺️ 외국인들이 좋아하는 서울 관광지 TOP 10")

# 관광지 데이터 (가장 가까운 지하철역 포함)
places = [
    {"name": "경복궁", "lat": 37.579617, "lon": 126.977041, 
     "desc": "조선의 대표 궁궐로, 한국 전통 건축의 아름다움이 살아있는 곳입니다.",
     "station": "경복궁역 (3호선)"},
    {"name": "북촌한옥마을", "lat": 37.582604, "lon": 126.983998, 
     "desc": "한옥이 잘 보존된 서울의 전통 마을로, 한국의 옛 주거 문화를 체험할 수 있습니다.",
     "station": "안국역 (3호선)"},
    {"name": "명동", "lat": 37.563757, "lon": 126.982690, 
     "desc": "패션, 화장품, 음식 등으로 외국인들에게 가장 인기 있는 쇼핑 거리입니다.",
     "station": "명동역 (4호선)"},
    {"name": "남산타워 (N서울타워)", "lat": 37.551169, "lon": 126.988227, 
     "desc": "서울의 랜드마크로, 도시 전경을 한눈에 볼 수 있으며 사랑의 자물쇠로도 유명합니다.",
     "station": "명동역 (4호선)"},
    {"name": "동대문디자인플라자 (DDP)", "lat": 37.566474, "lon": 127.009161, 
     "desc": "현대적인 건축물과 전시, 야경으로 인기 있는 디자인 복합 문화공간입니다.",
     "station": "동대문역사문화공원역 (2,4,5호선)"},
    {"name": "홍대거리", "lat": 37.556361, "lon": 126.922613, 
     "desc": "젊음과 예술의 거리로 버스킹, 클럽, 카페 문화가 발달한 지역입니다.",
     "station": "홍대입구역 (2호선, 공항철도, 경의중앙선)"},
    {"name": "이태원", "lat": 37.534596, "lon": 126.994834, 
     "desc": "다양한 외국 문화와 음식이 공존하는 서울의 글로벌 거리입니다.",
     "station": "이태원역 (6호선)"},
    {"name": "청계천", "lat": 37.569013, "lon": 126.978374, 
     "desc": "도심 속 휴식공간으로 야경 산책 코스로 인기가 많습니다.",
     "station": "광화문역 (5호선)"},
    {"name": "롯데월드타워", "lat": 37.513068, "lon": 127.102538, 
     "desc": "세계에서 가장 높은 빌딩 중 하나로, 전망대와 쇼핑, 엔터테인먼트를 즐길 수 있습니다.",
     "station": "잠실역 (2호선, 8호선)"},
    {"name": "한강공원 (여의도)", "lat": 37.528570, "lon": 126.932680, 
     "desc": "서울 시민과 관광객 모두가 즐기는 대표적인 한강 명소입니다.",
     "station": "여의나루역 (5호선)"}
]

# 지도를 서울 중심으로 설정
m = folium.Map(location=[37.56, 126.98], zoom_start=12)

# 마커 색상 순환 리스트
colors = ["red", "blue", "green", "purple", "orange", "darkred", 
          "lightred", "beige", "darkblue", "cadetblue"]

# 마커 추가
for i, place in enumerate(places):
    folium.Marker(
        location=[place["lat"], place["lon"]],
        popup=f"<b>{place['name']}</b><br>{place['desc']}<br><i>📍 가장 가까운 지하철역: {place['station']}</i>",
        tooltip=place["name"],
        icon=folium.Icon(color=colors[i % len(colors)], icon="star")
    ).add_to(m)

# 지도 표시
st_folium(m, width=1200, height=700)

# 구분선
st.markdown("---")

# 관광지 설명 섹션
st.subheader("📖 왜 이곳이 유명할까요?")
for i, place in enumerate(places, start=1):
    st.markdown(f"### {i}. {place['name']}")
    st.markdown(f"**가장 가까운 지하철역:** {place['station']}")
    st.markdown(f"**설명:** {place['desc']}")
    st.markdown("---")
