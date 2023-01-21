#!/usr/bin/python3
from flask import jsonify
from api.v1.views import app_views

@app_views.route('/status')
def status():
    """
    return the json "status": "ok"
    """
    data = {"status": "OK"}
    return jsonify(data)

@app_views.route('/stats')
def stats():
    """
    returns the number of all objects in JSON format
    """
    from models.amenity import Amenity
    from models.city import City
    from models.place import Place
    from models.review import Review
    from models.state import State
    from models.user import User
    from models import storage
    
    classes = {"amenities": Amenity,
            "cities": City,
            "places": Place, 
            "reviews": Review,
            "states": State,
            "users": User
            }
    class_count = {}
    for key, cls in classes.items():
        if storage.count(cls) is None:
            class_count[key] = 0
        else:
            class_count[key] = storage.count(cls)

    return jsonify(class_count)
