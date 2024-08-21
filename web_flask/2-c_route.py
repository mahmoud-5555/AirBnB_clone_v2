#!/usr/bin/python3
'''flask simple response'''
from flask import Flask


app = Flask(__name__)


@app.route('/')
def Hello_HBNB(strict_slashes=False):
    ''' function that act as api response '''
    return 'Hello HBNB!'


@app.route('/hbnb')
def HBNB(strict_slashes=False):
    ''' function that act as api response '''
    return 'HBNB'

@app.route('/c/', defaults={'text': None}, strict_slashes=False)
@app.route('/c/<text>')
def C(text, strict_slashes=False):
    ''' function that act as api response '''
    if text is not None:
        new = text.replace('_', ' ')
        return 'C ' + new


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5000')
