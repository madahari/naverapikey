import streamlit as st
import requests
import html
import re

# 기존 코드 주석 처리
# """
# # OpenAI API 설정
# openai_api_key = st.secrets["openai"]["api_key"]
# openai.api_key = openai_api_key

# def summarize_article(article):
#     prompt = f"Summarize the following news article: {article}"
#     try:
#         response = openai.ChatCompletion.create(
#             model="gpt-3.5-turbo",
#             messages=[
#                 {"role": "user", "content": prompt}
#             ]
#         )
#         return response.choices[0].message['content'].strip()
#     except Exception as e:
#         st.error(f"요약 생성 중 오류 발생: {e}")
#         return ""
# """
# 페이지 설정
st.set_page_config(page_title="네이버 키워드 기반 뉴스 검색", page_icon="📰")

# 네이버 뉴스 API 키 설정
client_id = st.secrets["naver"]["client_id"]
client_secret = st.secrets["naver"]["client_secret"]

# 뉴스 검색 함수
def search_news(keyword):
    encText = requests.utils.quote(keyword)
    url = f"https://openapi.naver.com/v1/search/news.json?query={encText}"
    headers = {
        "X-Naver-Client-Id": client_id,
        "X-Naver-Client-Secret": client_secret
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json().get('items', [])
    else:
        st.error("뉴스 검색에 실패했습니다.")
        return []

# 스트림릿 앱 구성
st.title("키워드 기반 뉴스 검색")

# 키워드 입력
keyword = st.text_input("관심 있는 뉴스 키워드를 입력하세요:")

# HTML 태그 제거 함수
def remove_html_tags(text):
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

# 뉴스 검색 및 표시
if st.button("뉴스 검색"):
    if keyword:
        news_list = search_news(keyword)
        for news in news_list:  
            title = html.unescape(news['title'])  # HTML 엔티티를 일반 텍스트로 변환
            title = remove_html_tags(title)  # HTML 태그 제거
            description = news['description']
            st.write(f"### {title}")  
            st.markdown(description, unsafe_allow_html=True)  # st.markdown으로 HTML 태그를 렌더링합니다
            st.write(f"[기사 읽기]({news['link']})")
            st.write("---")
    else:
        st.warning("키워드를 입력하세요.")
