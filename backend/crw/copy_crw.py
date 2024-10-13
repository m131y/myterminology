import requests
from bs4 import BeautifulSoup

URL = 'https://news.naver.com/main/list.naver?mode=LPOD&mid=sec&oid=003&listType=summary&date=20240327&page=2'

headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
}

response = requests.get(URL, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')

for news_item in soup.select('div.list_body ul li'):
        
    news_url = ''

    try:
        news_url = news_item.select('dt')[1].select_one('a').attrs['href']
    except:
        news_url = news_item.select('dt')[0].select_one('a').attrs['href']

    response = requests.get(news_url, headers=headers)
    news_soup = BeautifulSoup(response.text, 'html.parser')

    title = ''
    body = ''

    try:
        #일반기사
        title = news_soup.select_one('div.media_end_head_title h2#title_area').text.strip()
        body = news_soup.select_one('div.newsct_body div#newsct_article').text.strip().replace('\n','')
    except:    
        try:
            #스포츠기사
            title = news_soup.select_one('div.news_headline h4.title').text.strip()
            body = news_soup.select_one('div#newsEndContents').text.strip().replace('\n','')
        except:
            #연예기사
            title = news_soup.select_one('div.end_ct_area h2.end_tit').text.strip()
            body = news_soup.select_one('div.end_body_wrp div#articeBody').text.strip().replace('\n','')
   
    print(title)
    print('')
    print(body)
    print('')
    print('')  