#!/usr/bin/python3
'''flask simple response'''
from flask import Flask, abort


app = Flask(__name__)


@app.route('/', strict_slashes=False)
def Hello_HBNB():
    ''' function that act as api response '''
    return 'Hello HBNB!'


@app.route('/hbnb', strict_slashes=False)
def HBNB():
    ''' function that act as api response '''
    return 'HBNB'


@app.route('/c/<text>', strict_slashes=False)
def C(text):
    ''' function that act as api response '''
    if text is not None:
        new = text.replace('_', ' ')
        return 'C ' + new


@app.route('/python/', defaults={'text': None}, strict_slashes=False)
@app.route('/python/<text>')
def pytho(text, strict_slashes=False):
    ''' function that act as api response '''
    if text:
        new = text.replace('_', ' ')
        return 'Python ' + new
    else:
        return 'Python is cool'


@app.route('/number/<n>', strict_slashes=False)
def numberIsintger(n):
    n = str(n)
    if n.isdigit():
        return n + " is a number"
    abort(404)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5000',debug=True)
