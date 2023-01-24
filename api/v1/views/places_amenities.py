#!/usr/bin/python3
"""
link between Place objects and Ameity objects
handles all default RESTful API actions
"""
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.place import Place
from flask import abort, jsonify, request

@app_views.route('/places/<place_id>/amenities', methods=['GET'])
def place_amenity(place_id):
    """get amenities for a place and add amenity to a place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if request.method == 'GET':
        print(dir(place.amenities))
        amenities = [amenity.to_dict() for amenity in place.amenities]
        return jsonify(amenities)


@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['DELETE', 'POST'])
def place_amenities(place_id, amenity_id):
    """deletes and add amenities to a place"""
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if place is None or amenity is None:
        abort(404)
    if request.method == 'DELETE':
        for amenity in place.amenities:
            if amenity.id == amenity_id:
                place.amenities.remove(amenity)
                place.save()
                return jsonify({})
        abort(404)
    if request.method == 'POST':
        for amen in place.amenities:
            if amen.id == amenity.id:
                return jsonify(amenity.to_dict())
        place.amenities.append(amenity)
        place.save()
        return jsonify(amenity.to_dict()), 201
