#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
import os
from api.v1.auth.auth import Auth
from api.v1.auth.basic_auth import BasicAuth


app = Flask(__name__)
auth = None
app.register_blueprint(app_views)

CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
if os.getenv('AUTH_TYPE'):
    if os.getenv('AUTH_TYPE') == 'basic_auth':
        auth = BasicAuth()
    else:
        auth = Auth()


@app.before_request
def before_request():
    """the function that is processed before we process the request"""
    if auth is None:
        return
    excluded_paths = ['/api/v1/status/',
                      'api/v1/unauthorized/', '/api/v1/forbidden/']
    if not auth.require_auth(request.path, excluded_paths):
        return
    if auth.authorization_header(request) is None:
        abort(401)
    if auth.current_user(request) is None:
        abort(403)


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized(error) -> str:
    """ Not authorized handler
    """
    response = jsonify({"error": "Unauthorized"})
    response.status_code = 401
    return response


@app.errorhandler(403)
def unauthorized(error) -> str:
    """ Forbidden handler
    """
    response = jsonify({"error": "Forbidden"})
    response.status_code = 403
    return response


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
