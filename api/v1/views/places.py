#!/usr/bin/python3
""" defines routes that contain places string"""
from api.v1.views import app_views
from models import storage
from models.city import City
from models.place import Place
from models.state import State
from models.user import User
from flask import abort, jsonify, request


@app_views.route('/cities/<city_id>/places', methods=['GET', 'POST'])
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


def get_places(states, cities):
    """gets places from the id of states and cities"""
    places = []
    for state_id in states:
        state = storage.get(State, state_id)
        if state is not None:
            for city in state.cities:
                cities.append(city.id)
    for city_id in cities:
        city = storage.get(City, city_id)
        if city is not None:
            for place in city.places:
                places.append(place)
    return places


@app_views.route('/places_search', methods=['POST'])
def places_search():
    """get places depending on the state, cities and amenities passed as JSON"""
    filtr = request.get_json()
    places = []
    if type(filtr) != dict:
        return "Not a JSON\n", 400

    if len(filtr) == 0 or ((filtr.get('states') is None or len(filtr.get('states')) == 0) and (filtr.get('cities') is None or len(filtr.get('cities')) == 0)):
        places = [place for place in storage.all("Place").values()]
    else:
        states = [state for state in filtr.get('states', [])]
        cities = [city for city in filtr.get('cities', [])]
        places = get_places(states, cities)

    amenities_id = filtr.get('amenities')
    if amenities_id is not None:
        if len(amenities_id) > 0:
            new_place_list = []
            for place in places:
                place_amenity = []
                for amenity in place.amenities:
                    place_amenity.append(amenity.id)
                if all(x in place_amenity for x in amenities_id):
                    new_place_list.append(place.id)
            storage.close()
            places = [storage.get(Place, place) for place in new_place_list]
    places = [place.to_dict() for place in places]

    return jsonify(places)
