from flask import Flask
from flask import render_template
from flask import jsonify
import json

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/test1")
def test1():
    return "test1"

@app.route("/test2")
def test2():
    return render_template("test2.html")

@app.route("/test3")
def test3():
    return render_template("test3.html", data='test3')

@app.route("/test4")
def test4():
    list = [1,2,3,4]
    return render_template("test4.html", list=list)

@app.route("/test5")
def test5():
    dict_data = {"name":"cos", "phone":"01022228888"}
    return render_template("test5.html", dict_data=dict_data)

@app.route("/test6")
def test6():
    dict_data = {"name":"cos", "phone":"01022228888"}
    json_data = json.dumps(dict_data)
    return render_template("test6.html", json_data=json_data)

@app.route("/test7")
def test7():
    dict_data = {"name":"cos", "phone":"01022228888"}
    #json_data = json.dumps(dict_data) 요거 쓰면 안됨!!
    return jsonify(dict_data)

@app.route("/test8")
@app.route("/test8/<yourname>")
def test8(yourname="홍길동"):
    return yourname

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)