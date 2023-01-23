#!/usr/bin/python3
"""defines all routes to state"""

from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.state import State


@app_views.route('/states/', methods=['GET', 'POST'])
def states():
    """returns list of all states"""
    if request.method == 'GET':
        state_list = [
            state.to_dict() for state in storage.all('State').values()
            ]
        return jsonify(state_list)
    if request.method == 'POST':
        state = request.get_json()

        if type(state) != dict:
            return "Not a JSON\n", 400
        if 'name' not in state.keys():
            return "Missing name\n", 400
        new_state = State(**state)
        new_state.save()
        return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['GET', 'PUT', 'DELETE'])
def get_state(state_id):
    """gets a specific state and return it in json format"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if request.method == 'GET':
        return jsonify(state.to_dict())
    if request.method == 'DELETE':
        storage.delete(state)
        storage.save()
        return jsonify({})
    if request.method == 'PUT':
        new_info = request.get_json()
        if type(new_info) != dict:
            return "Not a JSON", 400
        for k, v in new_info.items():
            if k != 'updated_at' and k != 'created_at' and k != 'id':
                setattr(state, k, v)
        state.save()
        return jsonify(state.to_dict())
