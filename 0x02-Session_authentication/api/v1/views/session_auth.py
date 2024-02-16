#!/usr/bin/env python3
""" Module of session views
"""
import os
from api.v1.views import app_views
from flask import abort, jsonify, request, make_response
from models.user import User
from api.v1.app import auth


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login() -> str:
    """ POST /api/v1/auth_session/login
    JsonBody:
        - email
        - password
    Return:
      - return the user object
    """
    email = None
    password = None
    error_msg = None
    try:
        email = request.form.get('email')
        password = request.form.get('password')
    except Exception as e:
        email = None
        password = None

    if email is None or len(email) == 0:
        return jsonify({"error": "email missing"}), 400

    if password is None or len(password) == 0:
        return jsonify({"error": "password missing"}), 400

    users = User.search({"email": email})
    if not users:
        return jsonify({"error": "no user found for this email"}), 404

    user = users[0]
    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    # from api.v1.auth.session_auth import SessionAuth
    from api.v1.app import auth

    print(type(user.id))
    # session_id = SessionAuth.create_session(user.id)
    session_id = auth.create_session(user.id)

    if session_id is None:
        return jsonify({"error": "session ID creation failed"}), 500

    session_cookie_name = os.getenv('SESSION_NAME')
    res = make_response(user.to_json())
    res.set_cookie(session_cookie_name, session_id)

    return res


@app_views.route('/auth_session/logout',
                 methods=['DELETE'],
                 strict_slashes=False)
def del_session():
    """"
    function to destroy session
    """
    if not auth.destroy_session(request):
        abort(404)

    return jsonify({}), 200
