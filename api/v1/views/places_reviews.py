#!/usr/bin/python3
""" defines routes that contain places string"""
from api.v1.views import app_views
from models import storage
from models.review import Review
from models.place import Place
from flask import abort, jsonify, request

@app_views.route('/places/<place_id>/reviews', methods=['GET', 'DELETE'])
def reviews(place_id):
    """defines route to add and display all reviews"""
    place = storage.get(Place, place_id)
    if request.method == 'GET':
        reviews = [review.to_dict() for review in place.reviews]
        return jsonify(reviews)
    if request.method == 'POST':
        review_dict = request.get_json()
        if type(review_dict) != dict:
            return "Not a JSON\n", 400
        if 'user_id' not in review_dict.keys():
            return "Missing user_id", 400
        user = storage.get(User, review_dict.get('user_id', None))
        if user is None:
            abort(404)
        if 'text' not in review_dict.keys():
            return "Missing text", 400
        review_dict['place_id'] = place_id
        new_review = Place(**review_dict)
        new_review.save()
        return jsonify(new_review.to_dict()), 201
@app_views.route('/reviews/<review_id>', methods=['GET', 'DELETE', 'PUT'])
def get_review(review_id):
    """displays, delete and updates a specific place object"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    if request.method == 'GET':
        return jsonify(review.to_dict())
    if request.method == 'DELETE':
        storage.delete(review)
        storage.save()
        return jsonify({})
    if request.method == 'PUT':
        new_data = request.get_json()
        if type(new_data) != dict:
            return "Not a JSON", 400
        for k, v in new_data.items():
            if k != 'updated_at' and k != 'created_at' and k != 'id':
                setattr(review, k, v)
        review.save()
        return jsonify(review.to_dict())
