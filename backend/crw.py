import sys
import requests
from bs4 import BeautifulSoup
from newspaper import Article

# 커맨드 라인에서 입력받은 URL을 변수로 지정
URL = sys.argv[1]

# HTTP 요청 헤더
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'
}

# HTTP GET 요청을 통해 웹 페이지 가져오기
response = requests.get(URL, headers=headers)

# BeautifulSoup을 사용하여 HTML 파싱
news_soup = BeautifulSoup(response.text, 'html.parser')

# 기사 제목과 본문을 저장할 변수 초기화
title = ''
body = ''

# 네이버 뉴스 기사 크롤링
if 'n.news.naver.com' in URL:
    try:
        title = news_soup.select_one('div.media_end_head_title h2#title_area').text.strip()
        body = news_soup.select_one('div.newsct_body div#newsct_article').text.strip()
    except Exception as e:
        print(f"네이버 뉴스 크롤링 중 오류 발생: {e}")

# 네이버 뉴스가 아닌 경우 newspaper 모듈을 사용하여 크롤링
else:
    try:
        article = Article(URL)
        article.download()
        article.parse()
        title = article.title
        body = article.text
    except Exception as e:
        print(f"기사 크롤링 중 오류 발생: {e}")


# # 결과를 파일에 저장
with open('title.txt', 'w', encoding='utf-8') as title_file:
    title_file.write(title)
with open('body.txt', 'w', encoding='utf-8') as body_file:
    body_file.write(body)
