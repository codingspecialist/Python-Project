#-*- coding: utf-8 -*-

# 라이브러리를 로드합니다.
import requests
from bs4 import BeautifulSoup
import pymysql

#DB연결
db = pymysql.connect(host='localhost', port=3306, user='root', passwd='bitc5600', db='cos', charset='utf8')
#커서 생성 - 커서란:데이터를 엑세스할 때 필요!! - 결과집합의 첫번째 튜플=레코드
cursor = db.cursor()

def crawling(page):
    #파일이즈 영화 636페이지까지 11.07 14시기준
    url = 'http://fileis.com/contents/index.htm?category1=MVO&category2=&s_word=&viewTab=new&viewList=&rows=25&page='+str(page)

    r = requests.get(url)
    soup=BeautifulSoup(r.content,"html.parser")  
    titles = soup.select('.title .ellipsis a')

    items = []
    #공백제거
    for title in titles:
        clear_title = title.text.replace(" ", "")
        items.append(clear_title)

    for item in items:
        sql = f"INSERT INTO movie(title,gubun) VALUES('{item}',1)"
        cursor.execute(sql)

#range는 637전까지 반복함.
for page in range(1,637):
    print(str(page)+'/636')
    crawling(page)

db.commit()