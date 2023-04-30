#!/usr/bin/python3
"""View for State objects that handles all default RESTFul API actions
"""

from api.v1.views import app_views
from models import storage
from models.city import City
from models.user import User
from models.place import Place
from flask import jsonify, request, abort


@app_views.route("/cities/<city_id>/places",
                 methods=["GET", "POST"], strict_slashes=False)
def get_place_by_city_id(city_id):
    city_objs = storage.all(City).values()
    city_exists = False
    for city_obj in city_objs:
        if city_obj.id == city_id:
            city_exists = True
            break
    if not city_exists:
        abort(404)
    if request.method == "GET":
        place_objs = storage.all(Place).values()
        list_dict = [obj.to_dict() for obj in place_objs if
                     obj.city_id == city_id]
        return jsonify(list_dict), 200
    elif request.method == "POST":
        my_dict = request.get_json()
        if not my_dict or type(my_dict) is not dict:
            abort(400, "Not a JSON")
        if not my_dict.get('user_id'):
            abort(400, "Missing user_id")
        if not my_dict.get('name'):
            abort(400, "Missing name")
        user_objs = storage.all(User).values()
        user_exists = False
        for user_obj in user_objs:
            if user_obj.id == my_dict["user_id"]:
                user_exists = True
                break
        if not user_exists:
            abort(404)
        else:
            my_dict["city_id"] = city_id
            obj = Place(**my_dict)
            obj.save()
            return jsonify(obj.to_dict()), 201


@app_views.route("/places/<place_id>",
                 methods=["GET", "DELETE", "PUT"], strict_slashes=False)
def get_place_by_place_id(place_id):
    place_obj = storage.get(Place, place_id)
    if place_obj is None:
        abort(404)
    if request.method == "GET":
        return jsonify(place_obj.to_dict())
    elif request.method == "DELETE":
        storage.delete(place_obj)
        storage.save()
        return jsonify({}), 200
    elif request.method == "PUT":
        my_dict = request.get_json()
        if not my_dict or type(my_dict) is not dict:
            abort(400, "Not a JSON")
        place_obj.__dict__.update(my_dict)
        place_obj.save()
        return jsonify(place_obj.to_dict()), 201
