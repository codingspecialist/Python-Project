#-*- coding: utf-8 -*-

# 라이브러리를 로드합니다.
import requests
from bs4 import BeautifulSoup

#파일이즈 영화 636페이지까지 11.07 14시기준
url = 'http://fileis.com/contents/index.htm?category1=MVO&category2=&s_word=&viewTab=new&viewList=&rows=25&page=1'

r = requests.get(url)
soup=BeautifulSoup(r.content,"html.parser")  
titles = soup.select('.title .ellipsis a')

items = []
#공백제거
for title in titles:
        clear_title = title.text.replace(" ", "")
        print(clear_title)
        items.append(clear_title)
                
    
    