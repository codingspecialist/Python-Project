from flask import Flask, redirect, url_for
from flask import render_template 
from flask import request
from callApi import get_busStop
from callApi import get_stopArr
from callApi import get_busInfo
from callApi import get_busLocation

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('main.html')

@app.route('/lineform')
def lineform():
    return render_template('lineform.html')

@app.route('/get_bstopId', methods=['POST'])
def get_bstopid():
    bstopnm = request.form['bstopnm']
    list = get_busStop(bstopnm)
    return render_template('lineform.html', list=list)

@app.route('/get_stoplist/<bstopId>')
def get_stoplist(bstopId):
    list = get_stopArr(bstopId)
    return render_template('stoplist.html', list=list)

@app.route('/buslocationform')
def buslocationform():
    return render_template('buslocationform.html')    

@app.route('/get_buslocation', methods=['POST'])
def get_buslocation():
    buslinenum = request.form['buslinenum']
    lineId = get_busInfo(buslinenum)
    list = get_busLocation(lineId)
    return render_template('buslocationform.html', list=list) 

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)