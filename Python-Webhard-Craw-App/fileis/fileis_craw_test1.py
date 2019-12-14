#-*- coding: utf-8 -*-

# 라이브러리를 로드합니다.
import requests
from bs4 import BeautifulSoup

#파일이즈 영화 636페이지까지 11.07 14시기준
url = "http://fileis.com/contents/index.htm?category1=MVO#2"

r = requests.get(url)
print(r.text)


