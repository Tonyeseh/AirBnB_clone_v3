#!/usr/bin/python3
"""Defines all routes that manipulates amenity object"""
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from flask import abort, jsonify, request


@app_views.route('/amenities', methods=['GET', 'POST'])
def amenities():
    """gets and adds amenities to the storage"""
    if request.method == 'GET':
        amenities = [
            amenity.to_dict() for amenity in storage.all('Amenity').values()
            ]
        return jsonify(amenities)
    if request.method == 'POST':
        amenity_dict = request.get_json()
        if type(amenity_dict) != dict:
            return "Not a JSON\n", 400
        if 'name' not in amenity_dict.keys():
            return "Missing name\n", 400
        amenity = Amenity(**amenity_dict)
        amenity.save()
        return jsonify(amenity.to_dict())

@app_views.route('/amenities/<amenity_id>', methods=['GET', 'DELETE', 'PUT'])
def get_amenity(amenity_id):
    """gets a specific amenity displays, delete or update it"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    if request.method == 'GET':
        return jsonify(amenity.to_dict())
    if request.method == 'DELETE':
        storage.delete(amenity)
        storage.save()
        return jsonify({})
    if request.method == 'PUT':
        new_data = request.get_json()
        if type(new_data) != dict:
            return "Not a JSON\n", 400
        for k, v in new_data.items():
            if k != 'updated_at' and k != 'created_at' and k != 'id':
                setattr(amenity, k, v)
        amenity.save()
        return jsonify(amenity.to_dict())
