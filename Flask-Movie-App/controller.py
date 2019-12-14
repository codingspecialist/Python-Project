from jsonProcess import getMovie
from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route('/')
def index():
    return 'Welcome index page'

@app.route('/movie/<page>')
@app.route('/movie/')
def movie(page='1'):
    list = getMovie(page)
    return render_template('movie.html', list=list, page=int(page))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=9000, debug=True)

