from flask import Flask
from flask import render_template 
from flask import request
import pymysql

#데이터베이스연결
db = pymysql.connect(host='localhost', port=3306, user='root', passwd='bitc5600', db='cos', charset='utf8')
#커서생성
cursor = db.cursor()

app = Flask(__name__)

@app.route('/')
def cluster():
    #cctv데이터
    sql = "SELECT * FROM cctv"
    cursor.execute(sql)
    rs = cursor.fetchall()
    rs = list(rs)
    return render_template('cctv_clustering.html', rs=rs)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)