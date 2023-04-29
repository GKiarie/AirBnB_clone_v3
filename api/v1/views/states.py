#!/usr/bin/python3
"""View for State objects that handles all default RESTFul API actions
"""

from api.v1.views import app_views
from models import storage
from models.state import State
from flask import jsonify, request, abort


@app_views.route("/states", methods=["GET", "POST"], strict_slashes=False)
@app_views.route("/states/<state_id>",
             methods=["GET", "DELETE", "PUT"], strict_slashes=False)
def get_all_states(state_id=None):
    state_objs = storage.all(State).values()
    obj_dicts = [obj.to_dict() for obj in state_objs]
    if not state_id:
        if request.method == "GET":
            return jsonify(obj_dicts), 200
        elif request.method == "POST":
            my_dict = request.get_json()
            if not my_dict:
                abort(400, "Not a JSON")
            if not my_dict.get('name'):
                abort(400, "Missing name")
            else:
                obj = State(**my_dict)
                obj.save()
                return jsonify(obj.to_dict()), 201
    else:
        obj = storage.get(State, state_id)
        if not obj:
            abort(404)
        if request.method == "GET":
            return jsonify(storage.get(State, state_id).to_dict()), 200
        elif request.method == "PUT":
            my_dict = request.get_json()
            if not my_dict:
                abort(400, "Not a JSON")
            else:
                obj = State(**my_dict)
                obj.save()
                return jsonify(obj.to_dict()), 201
        elif request.method == "DELETE":
            storage.delete(obj)
            storage.save()
            return jsonify({}), 200
