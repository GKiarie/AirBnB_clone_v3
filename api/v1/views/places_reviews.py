#!/usr/bin/python3
"""View for State objects that handles all default RESTFul API actions
"""

from api.v1.views import app_views
from models import storage
from models.city import City
from models.review import Review
from models.user import User
from models.place import Place
from flask import jsonify, request, abort


@app_views.route("/places/<place_id>/reviews",
                 methods=["GET", "POST"], strict_slashes=False)
def get_review_by_place_id(place_id):
    place_objs = storage.all(Place).values()
    place_exists = False
    for place_obj in place_objs:
        if place_obj.id == place_id:
            place_exists = True
            break
    if not place_exists:
        abort(404)
    if request.method == "GET":
        review_objs = storage.all(Review).values()
        list_dict = [obj.to_dict() for obj in review_objs if
                     obj.place_id == place_id]
        return jsonify(list_dict), 200
    elif request.method == "POST":
        my_dict = request.get_json()
        if not my_dict or type(my_dict) is not dict:
            abort(400, "Not a JSON")
        if not my_dict.get('user_id'):
            abort(400, "Missing user_id")
        if not my_dict.get('text'):
            abort(400, "Missing text")
        user_objs = storage.all(User).values()
        user_exists = False
        for user_obj in user_objs:
            if user_obj.id == my_dict["user_id"]:
                user_exists = True
                break
        if not user_exists:
            abort(404)
        else:
            my_dict["place_id"] = place_id
            obj = Review(**my_dict)
            obj.save()
            return jsonify(obj.to_dict()), 201


@app_views.route("/reviews/<review_id>",
                 methods=["GET", "DELETE", "PUT"], strict_slashes=False)
def get_review_by_review_id(review_id):
    review_obj = storage.get(Review, review_id)
    if review_obj is None:
        abort(404)
    if request.method == "GET":
        return jsonify(review_obj.to_dict())
    elif request.method == "DELETE":
        storage.delete(review_obj)
        storage.save()
        return jsonify({}), 200
    elif request.method == "PUT":
        my_dict = request.get_json()
        if not my_dict or type(my_dict) is not dict:
            abort(400, "Not a JSON")
        review_obj.__dict__.update(my_dict)
        review_obj.save()
        return jsonify(review_obj.to_dict()), 201
