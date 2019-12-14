from flask import Flask
from flask import render_template 
from flask import request
import pymysql
from urllib.parse import urlencode
import requests
import json

#데이터베이스연결
db = pymysql.connect(host='localhost', port=3306, user='root', passwd='bitc5600', db='cos', charset='utf8')
#커서생성
cursor = db.cursor()

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/weather', methods=['POST'])
def weather():
    addr = request.form['addr']
    sql = f"select max(y), max(x) from coordinate where addr3 like '%{addr}%';"
    cursor.execute(sql)
    rs1 = cursor.fetchone()
    r_item = get_weather(rs1[0], rs1[1])
    return render_template('weather.html', r_item=r_item)

def get_weather(ny=127,nx=60):
    url = 'http://newsky2.kma.go.kr/service/SecndSrtpdFrcstInfoService2/ForecastSpaceData'
    queryParams = '?' + urlencode({'ServiceKey' : 'wJmmW29e3AEUjwLioQR22CpmqS645ep4S8TSlqtSbEsxvnkZFoNe7YG1weEWQHYZ229eNLidnI2Yt5EZ3Stv7g==', 'base_date' : '20181110', 'base_time' : '0500', 'nx' : nx, 'ny' : ny, 'numOfRows' : '10', 'pageNo' : '1', '_type' : 'json' })

    response = requests.get(url + queryParams)
    r_dict = json.loads(response.text)

    if response.status_code == 200:
        r_response = r_dict['response']
        r_body = r_response['body']
        r_items = r_body['items']
        r_item = r_items['item']
        return r_item

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)