import requests
from urllib.parse import urlencode
import json
from urllib.parse import quote_plus

#정류소 정보 조회(수영역을 치면 해당역 근처에 버스정류장 GPS가져올 수 있음)
def get_busStop(bstopnm):
    url = 'http://61.43.246.153/openapi-data/service/busanBIMS2/busStop'
    queryParams = '?' + urlencode({ quote_plus('ServiceKey') : 'wJmmW29e3AEUjwLioQR22CpmqS645ep4S8TSlqtSbEsxvnkZFoNe7YG1weEWQHYZ229eNLidnI2Yt5EZ3Stv7g==', quote_plus('bstopnm') : bstopnm, '_type' : 'json'})
    response = requests.get(url + queryParams)
    r_dict = json.loads(response.text)

    if response.status_code == 200:
         r_response = r_dict['response']
         r_body = r_response['body']
         r_items = r_body['items']
         r_item = r_items['item']
         #print(r_item)
         return r_item

#정류소 도착정보 조회 (수영역 정류장에 몇분 뒤에 버스들이 도착하는지 확인가능)
def get_stopArr(bstopid):
    url = 'http://61.43.246.153/openapi-data/service/busanBIMS2/stopArr'
    queryParams = '?' + urlencode({ quote_plus('ServiceKey') : 'wJmmW29e3AEUjwLioQR22CpmqS645ep4S8TSlqtSbEsxvnkZFoNe7YG1weEWQHYZ229eNLidnI2Yt5EZ3Stv7g==', quote_plus('bstopid') : bstopid, '_type' : 'json' })
    response = requests.get(url + queryParams)
    r_dict = json.loads(response.text)

    if response.status_code == 200:
         r_response = r_dict['response']
         r_body = r_response['body']
         r_items = r_body['items']
         r_item = r_items['item']

         #print(r_item)
         return r_item

#노선 정보 조회(51번 버스 조회 -> 버스ID 확인가능)
def get_busInfo(buslinenum):
    url = 'http://61.43.246.153/openapi-data/service/busanBIMS2/busInfo'
    queryParams = '?' + urlencode({ quote_plus('ServiceKey') : 'wJmmW29e3AEUjwLioQR22CpmqS645ep4S8TSlqtSbEsxvnkZFoNe7YG1weEWQHYZ229eNLidnI2Yt5EZ3Stv7g==', 'lineno':buslinenum, '_type' : 'json'})

    response = requests.get(url + queryParams)
    r_dict = json.loads(response.text)

    r_response = r_dict['response']
    r_body = r_response['body']
    r_items = r_body['items']
    r_item = r_items['item']
    print(r_item)
    if type(r_item) == list:
        return r_item[0]['lineId']
    else:
        return r_item['lineId']

#노선 정류소 조회(버스ID 조회 -> 51번 버스 정류장 조회 및 실시간 위치 확인)
def get_busLocation(lineId):
    url = 'http://61.43.246.153/openapi-data/service/busanBIMS2/busInfoRoute'
    queryParams = '?' + urlencode({ quote_plus('ServiceKey') : 'wJmmW29e3AEUjwLioQR22CpmqS645ep4S8TSlqtSbEsxvnkZFoNe7YG1weEWQHYZ229eNLidnI2Yt5EZ3Stv7g==', quote_plus('lineid') : lineId, '_type' : 'json' })
    response = requests.get(url + queryParams)
    r_dict = json.loads(response.text)

    r_response = r_dict['response']
    r_body = r_response['body']
    r_items = r_body['items']
    r_item = r_items['item']
    #print(r_item)
    return r_item