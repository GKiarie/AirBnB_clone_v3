#!/usr/bin/python3
"""App module"""

from models import storage
from api.v1.views import app_views
from flask import Flask
import os


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def close_storage(error):
    """
    @app.teardown_appcontext: registers a ftn to be torn
    down when app context is tron down.
    close_storage(): closes storage in use
    """
    storage.close()


if __name__ == "__main__":
    app.run(host=os.getenv('HBNB_API_HOST', '0.0,0,0'),
            port=int(os.getenv('HBNB_API_PORT', '5000')),
            threaded=True)
