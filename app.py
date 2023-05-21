import streamlit as st
import requests
from requests.exceptions import JSONDecodeError
import urllib.parse

API_ENDPOINT = "http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0"
API_KEY = "d0mP886Qs5a3Y4SvZex0oXe%2FDGPx%2BkWUzw8y8sym7k23cQ2tIrgqsiK5TvbotTaODr74xm3rCD5wy899P%2BoTSg%3D%3D"

def fetch_weather_data(city):
    url = f"{API_ENDPOINT}?serviceKey={API_KEY}&city={city}"
    
    try:
        response = requests.get(url)
        data = response.json()
        return data
    except JSONDecodeError as e:
        st.error("기상청 API 응답 처리 오류: 올바른 응답 형식이 아닙니다.")
        st.error(str(e))
        return None

st.title("기상 정보 조회")
city = st.text_input("도시 입력", "서울")

if st.button("조회"):
    weather_data = fetch_weather_data(city)
    
    if weather_data:
        st.subheader(f"{city}의 기상 정보")
        st.write(weather_data)
