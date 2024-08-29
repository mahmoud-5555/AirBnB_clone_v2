#!/usr/bin/python3
'''flask simple response'''
from flask import Flask, render_template
from models import storage
from models.engine.db_storage import DBStorage
from models.engine.file_storage import FileStorage


app = Flask(__name__)


@app.teardown_appcontext
def reconect_DP(exception=None):
    """Cleanup tasks after each request."""
    storage.close()


@app.route('/cities_by_states', strict_slashes=False)
def allStatesView():
    from models.state import State
    from models.city import City
    ''''method to response all states request'''
    data_states = storage.all(State)
    data_cities =  storage.all(City)
    data_results = [] 
    """
    data_results:
    type : list of dict "states" | key(tuple("id of the state"
    , "name of the staes")) | value("list of tuple(city's id, city's name)")
    """
    # group the data
    for i in data_states:
        element = dict() # var to make an states  
        key = tuple(i.id, i.name)
        element[key] = []  #State element
        for j in data_cities:
            if i.id == j.state_id:
				# add new value to the states | City : tuple(id , name)
                element[key].append(tuple(j.id, j.name))
        # After done of the element sort the cities in side the states 
        element[key] = sorted(element[key], key= lambda a: a[1])
        data_results.append(element)
    # Sort the States  
    data_results = sorted(data_results, key= lambda a: a.key()[0][1])
    
    return render_template('', respo=data_results)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5000')
