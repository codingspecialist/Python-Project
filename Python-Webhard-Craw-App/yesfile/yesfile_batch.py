#-*- coding: utf-8 -*-

# 라이브러리를 로드합니다.
import requests
import json
import pymysql
import coolsms

#DB연결
db = pymysql.connect(host='localhost', port=3306, user='root', passwd='bitc5600', db='cos', charset='utf8')
#커서 생성 - 커서란:데이터를 엑세스할 때 필요!! - 결과집합의 첫번째 튜플=레코드
cursor = db.cursor()

def crawling(page):
    #예스파일 영화 2501페이지까지 11.07 18시기준
    url = "https://www.yesfile.com/ajax/ajax_list.php?code=BD_MV&page="+str(page)+"&sec=1&start="+str((page-1)*20)+"&list_scale=20"

    r = requests.get(url)
    r_dict = json.loads(r.text)

    for titles in r_dict['list']:
        clear_title = titles['title'].replace(" ","")
        sql = "INSERT INTO movie(title,gubun) VALUES('"+clear_title+"',2)"
        cursor.execute(sql)
        if clear_title.find('신과함께2') != -1:
            coolsms.sendSMS(clear_title)

for i in range(1,5):
    crawling(i)

db.commit()
