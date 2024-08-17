#!/usr/bin/python3
'''flask simple response'''
from flask import Flask

app =  Flask(__name__)

@app.route('/')
def Hello_HBNB(strict_slashes=False):
    ''' function that act as api response '''
    return 'Hello HBNB!'

if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5000')
