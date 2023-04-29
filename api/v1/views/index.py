#!/usr/bin/python3
"""Module for app views"""

from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status')
def status():
    """view for /status route"""
    return jsonify({"status": "OK"})
