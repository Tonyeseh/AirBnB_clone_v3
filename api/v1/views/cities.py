#!/usr/bin/python3
"""Defines all the routes for city"""

from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.state import State
from models.city import City

@app_views.route('/states/<state_id>/cities', methods=['GET', 'POST'])
def state_cities(state_id):
    """returns a list of all cities in a state"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if request.method == 'GET':
        cities = [city.to_dict() for city in state.cities]
        return jsonify(cities)
    if request.method == 'POST':
        city_dict = request.get_json()
        if type(city_dict) != dict:
            return "Not a JSON\n", 400
        if 'name' not in city_dict.keys():
            return "Missing name\n", 400
        city_dict['state_id'] = state_id
        new_city = City(**city_dict)
        new_city.save()
        return jsonify(new_city.to_dict()), 201

@app_views.route('/cities/<city_id>', methods=['GET', 'DELETE', 'PUT'])
def all_cities(city_id):
    """returns a list of all ciites"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if request.method == 'GET':
        return jsonify(city.to_dict())
    if request.method == 'DELETE':
        storage.delete(city)
        storage.save()
        return jsonify({})
    if request.method == 'PUT':
        new_info = request.get_json()
        if type(new_info) != dict:
            return "Not a JSON", 400
        for k, v in new_info.items():
            if k != 'updated_at' and k != 'created_at' and k != 'id':
                setattr(city, k, v)
        city.save()
        return jsonify(city.to_dict())
