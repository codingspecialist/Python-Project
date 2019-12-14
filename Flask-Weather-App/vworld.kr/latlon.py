from urllib.parse import urlencode
import requests
import json

def get_latlon(addr):
    url = f"http://api.vworld.kr/req/address?service=address&request=getCoord&key=6D79E5D8-7966-39B9-B9D9-17BC968BBFF9&type=ROAD&address={addr}"
    response = requests.get(url)
    r_dict = json.loads(response.text)
    response = r_dict['response']
    result = response['result']
    point = result['point']
    print(point['x']) #경도 lon
    print(point['y']) #위도 lat = loc
    return point

#도로명으로 검색
point = get_latlon('광서로16번길')
#출력
print('위도 : '+point['y'])
print('경도 : '+point['x'])
