#!/usr/bin/python3
"""View for State objects that handles all default RESTFul API actions
"""

from api.v1.views import app_views
from models import storage
from models.user import User
from flask import jsonify, request, abort


@app_views.route("/users", methods=["GET", "POST"], strict_slashes=False)
@app_views.route("/users/<user_id>",
                 methods=["GET", "DELETE", "PUT"], strict_slashes=False)
def get_all_users(user_id=None):
    user_objs = storage.all(User).values()
    obj_dicts = [obj.to_dict() for obj in user_objs]
    if not user_id:
        if request.method == "GET":
            return jsonify(obj_dicts), 200
        elif request.method == "POST":
            my_dict = request.get_json()
            if not my_dict:
                abort(400, "Not a JSON")
            if not my_dict.get('email'):
                abort(400, "Missing email")
            if not my_dict.get('password'):
                abort(400, "Missing password")
            else:
                obj = User(**my_dict)
                obj.save()
                return jsonify(obj.to_dict()), 201
    else:
        obj = storage.get(User, user_id)
        if not obj:
            abort(404)
        if request.method == "GET":
            return jsonify(storage.get(User, user_id).to_dict()), 200
        elif request.method == "PUT":
            my_dict = request.get_json()
            if not my_dict:
                abort(400, "Not a JSON")
            else:
                ignore_keys = ["id", "email", "created_at", "updated_at"]
                my_dict = {key: value for key, value in my_dict.items() if key
                           not in ignore_keys}
                obj.__dict__.update(my_dict)
                obj.save()
                return jsonify(obj.to_dict()), 201
        elif request.method == "DELETE":
            storage.delete(obj)
            storage.save()
            return jsonify({}), 200
