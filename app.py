import streamlit as st
import requests
from requests.exceptions import RequestException
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
import seaborn as sns

API_ENDPOINT = "http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0"
API_KEY = "d0mP886Qs5a3Y4SvZex0oXe%2FDGPx%2BkWUzw8y8sym7k23cQ2tIrgqsiK5TvbotTaODr74xm3rCD5wy899P%2BoTSg%3D%3D"


def fetch_weather_data(city, base_date, base_time, nx, ny):
    url = f"{API_ENDPOINT}/getUltraSrtNcst"
    params = {
        'serviceKey': API_KEY,
        'pageNo': '1',
        'numOfRows': '10',
        'dataType': 'XML',
        'base_date': base_date,
        'base_time': base_time,
        'nx': nx,
        'ny': ny
    }
    
    try:
        response = requests.get(url, params=params)
        xml_data = response.content
        
        # XML 파싱
        root = ET.fromstring(xml_data)
        
        # 필요한 데이터 추출 및 처리
        data = extract_data_from_xml(root)
        
        return data
    except RequestException as e:
        st.error("기상청 API 응답 처리 오류: {}".format(str(e)))
        return None


def extract_data_from_xml(root):
    extracted_data = []
    
    # XML 파싱 및 데이터 추출
    for item in root.iter('item'):
        # 원하는 항목의 값을 추출하여 리스트에 추가
        category = item.findtext('category')
        fcst_time = item.findtext('fcstTime')
        fcst_value = item.findtext('fcstValue')
        extracted_data.append({'category': category, 'fcstTime': fcst_time, 'fcstValue': fcst_value})
    
    return extracted_data


st.title("기상 정보 조회")
city = st.text_input("도시 입력", "서울")
base_date = st.text_input("기준 날짜 입력 (예: 20210628)", "20210628")
base_time = st.text_input("기준 시간 입력 (예: 0600)", "0600")
nx = st.text_input("X 좌표 입력", "55")
ny = st.text_input("Y 좌표 입력", "127")

if st.button("조회"):
    weather_data = fetch_weather_data(city, base_date, base_time, nx, ny)
    
    if weather_data:
        st.subheader(f"{city}의 기상 정보")
        st.table(weather_data)
        
        # 차트 출력
        chart_type = st.selectbox("차트 유형", ["Line Plot", "Bar Plot"])
        
        if chart_type == "Line Plot":
            # Line Plot 생성
            plt.figure(figsize=(8, 6))
            for item in weather_data:
                fcst_time = item['fcstTime']
                fcst_value = float(item['fcstValue'])
                plt.plot(fcst_time, fcst_value, marker='o', label=item['category'])
            plt.xlabel('시간')
            plt.ylabel('값')
            plt.legend()
            st.pyplot(plt)
        elif chart_type == "Bar Plot":
            # Bar Plot 생성
            plt.figure(figsize=(8, 6))
            categories = [item['category'] for item in weather_data]
            fcst_values = [float(item['fcstValue']) for item in weather_data]
            sns.barplot(x=categories, y=fcst_values)
            plt.xlabel('카테고리')
            plt.ylabel('값')
            plt.xticks(rotation=45)
            st.pyplot(plt)

