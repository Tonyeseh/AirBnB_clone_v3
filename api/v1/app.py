#!/usr/bin/python3
"""defines the flask instance"""
from flask import Flask, jsonify
from flask_cors import CORS
from models import storage
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})
app.url_map.strict_slashes = False
app.register_blueprint(app_views, url_prefix='/api/v1')


@app.teardown_appcontext
def teardown(self):
    """
    closes and starts a new session
    """
    storage.close()


@app.errorhandler(404)
def error_404(err):
    """handles 404 errors"""
    return jsonify({"error": "Not found"}), 404


if __name__ == '__main__':
    host = '0.0.0.0'
    port = 5000
    if getenv("HBNB_API_HOST"):
        host == getenv("HBNB_API_HOST")
    if getenv("HBNB_API_PORT"):
        port = getenv("HBNB_API_PORT")
    app.run(host, port, threaded=True)
