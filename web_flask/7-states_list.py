#!/usr/bin/python3
'''flask simple response'''
from flask import Flask, render_template
from models import storage
from models.engine.db_storage import DBStorage
from models.engine.file_storage import FileStorage


app = Flask(__name__)


@app.teardown_appcontext
def teardown_appcontext(exception=None):
    """Cleanup tasks after each request."""
    storage.close()

@app.route('/states_list', strict_slashes=False)
def allStatesView():
    from models.state import State
    ''''method to response all states request'''
    data = storage.all(State)
    data = sorted(data.values(),key=lambda a: a.name)
    return render_template('7-states_list.html', respo=data)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5000')
