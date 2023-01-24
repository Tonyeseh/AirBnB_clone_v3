#!/usr/bin/python3
""" defines routes that contain places string"""
from api.v1.views import app_views
from models import storage
from models.city import City
from models.place import Place
from flask import abort, jsonify, request


@app_views.route('/cities/<city_id>/places', methods=['GET', 'DELETE'])
def places(city_id):
    """defines route to add and display all places"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if request.method == 'GET':
        places = [place.to_dict() for place in city.places]
        return jsonify(places)
    if request.method == 'POST':
        place_dict = request.get_json()
        if type(place_dict) != dict:
            return "Not a JSON\n", 400
        if 'user_id' not in place_dict.keys():
            return "Missing user_id", 400
        user = storage.get(User, place_dict.get('user_id', None))
        if user is None:
            abort(404)
        if 'name' not in place_dict.keys():
            return "Missing name", 400
        place_dict['city_id'] = city_id
        new_place = Place(**place_dict)
        new_place.save()
        return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['GET', 'DELETE', 'PUT'])
def get_place(place_id):
    """displays, delete and updates a specific place object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if request.method == 'GET':
        return jsonify(place.to_dict())
    if request.method == 'DELETE':
        storage.delete(place)
        storage.save()
        return jsonify({})
    if request.method == 'PUT':
        new_data = request.get_json()
        if type(new_data) != dict:
            return "Not a JSON", 400
        for k, v in new_data.items():
            if k != 'updated_at' and k != 'created_at' and k != 'id':
                setattr(place, k, v)
        place.save()
        return jsonify(place.to_dict())
