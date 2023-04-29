#!/usr/bin/python3
"""Python module - Blueprint"""

from flask import Blueprint

app_views = Blueprint("app_views", __name__, url_prefix='/api/v1')

from api.v1.views.index import *
