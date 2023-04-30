#!/usr/bin/python3
"""View for State objects that handles all default RESTFul API actions
"""

from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City
from flask import jsonify, request, abort


@app_views.route("/states/<state_id>/cities",
                 methods=["GET", "POST"], strict_slashes=False)
def get_city_by_state_id(state_id):
    state_objs = storage.all(State).values()
    state_exists = False
    for state_obj in state_objs:
        if state_obj.id == state_id:
            state_exists = True
            break
    if not state_exists:
        abort(404)
    if request.method == "GET":
        city_objs = storage.all(City).values()
        list_dict = [obj.to_dict() for obj in city_objs if
                     obj.state_id == state_id]
        return jsonify(list_dict), 200
    elif request.method == "POST":
        my_dict = request.get_json()
        if not my_dict or type(my_dict) is not dict:
            abort(400, "Not a JSON")
        if not my_dict.get('name'):
            abort(400, "Missing name")
        else:
            my_dict["state_id"] = state_id
            obj = City(**my_dict)
            obj.save()
            return jsonify(obj.to_dict()), 201


@app_views.route("/cities/<city_id>",
                 methods=["GET", "DELETE", "PUT"], strict_slashes=False)
def get_city_by_city_id(city_id):
    city_obj = storage.get(City, city_id)
    if city_obj is None:
        abort(404)
    if request.method == "GET":
        return jsonify(city_obj.to_dict())
    elif request.method == "DELETE":
        storage.delete(city_obj)
        storage.save()
        return jsonify({}), 200
    elif request.method == "PUT":
        my_dict = request.get_json()
        if not my_dict or type(my_dict) is not dict:
            abort(400, "Not a JSON")
        city_obj.__dict__.update(my_dict)
        city_obj.save()
        return jsonify(city_obj.to_dict()), 201
