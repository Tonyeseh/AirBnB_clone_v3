#!/usr/bin/python3
"""defines routes and mehtods that affects the user resource"""

from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET', 'POST'])
def users():
    """displays all users or add new user.. depending on the method"""
    if request.method == 'GET':
        users = [user.to_dict() for user in storage.all('User').values()]
        return jsonify(users)
    if request.method == 'POST':
        user_dict = request.get_json()
        if type(user_dict) != dict:
            return "Not a JSON\n", 400
        if 'email' not in user_dict.keys():
            return "Missing email\n", 400
        if 'password' not in user_dict.keys():
            return "Missing password\n", 400
        user = User(**user_dict)
        user.save()
        return jsonify(user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['GET', 'DELETE', 'PUT'])
def user(user_id):
    """outputs, delete, and update a specific user"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    if request.method == 'GET':
        return jsonify(user.to_dict())
    if request.method == 'DELETE':
        storage.delete(user)
        storage.save()
        return jsonify({})
    if request.method == 'PUT':
        user_dict = request.get_json()
        if type(user_dict) != dict:
            return "Not a JSON\n", 400
        for k, v in user_dict.items():
            if k != 'updated_at' and k != 'created_at' and k != 'id':
                setattr(user, k, v)
        user.save()
        return jsonify(user.to_dict())
