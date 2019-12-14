#-*- coding: utf-8 -*-

# 라이브러리를 로드합니다.
import requests

#예스파일 영화 2501페이지까지 11.07 18시기준
url = f'https://www.yesfile.com/ajax/ajax_list.php?code=BD_MV&page=1&sec=1&start=0&list_scale=20'

r = requests.get(url)
print(r.text)
            
   