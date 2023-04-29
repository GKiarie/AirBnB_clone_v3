#!/usr/bin/python3
"""Module for app views"""

from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status')
def status():
    """view for /status route"""
    return jsonify({"status": "OK"})


@app_views.route('/stats')
def retrieve_objects():
    """retrieve objects by type (Classes)"""
    resource_dict = {}
    classes = {"amenities": "Amenity", "cities": "City",
               "places": "Place", "reviews": "Review",
               "states": "State", "users": "User"}
    for key, value in classes.items():
        resource_dict[key] = storage.count(value)
    return jsonify(resource_dict)
