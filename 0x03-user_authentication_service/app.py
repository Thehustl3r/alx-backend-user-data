#!/usr/bin/env python3
"""app module"""
from flask import Flask, jsonify, request, abort, redirect, make_response
from auth import Auth


app = Flask(__name__)
auth = Auth()


@app.route("/", methods=['GET'], strict_slashes=False)
def welcome():
    """the welcome message"""
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=['POST'], strict_slashes=False)
def users():
    """POST /users/
        Json Body:
            - email: The email of the user
            - password: The password of the user
        Return:
            - User object represented
            - 400 when the user already exists
    """
    data = request.form
    email = data.get('email')
    password = data.get('password')
    try:
        auth.register_user(email, password)
        return jsonify({"email": email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login():
    """
    POST /sessions/
    JSON Body:
        - email: user email
        - password: user password
    Return:
        - Nothing
        - abort(401): when login fails
    """
    email = request.form.get('email')
    password = request.form.get('password')
    is_valid = auth.valid_login(email=email, password=password)
    if is_valid:
        session_id = auth.create_session(email=email)
        res = jsonify({"email": email, "message": "logged in"})
        res.set_cookie("session_id", session_id)
        return res, 200
    abort(401)


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout():
    """
    DELETE /sessions
    json body:
        - session_id:
    Return:
        - Nothing
    """
    session_id = request.cookies.get('session_id')
    user = auth.get_user_from_session_id(session_id=session_id)

    if user is not None:
        auth.destroy_session(user.id)
        return redirect("/", code=302)
    else:
        return jsonify({"error": "Forbidden"}), 403


@app.route('/profile/', methods=['GET'], strict_slashes=False)
def profile():
    """
    GET /provile/
    """
    session_id = request.cookies.get('session_id')
    user = auth.get_user_from_session_id(session_id)
    if user is not None:
        return jsonify({"email": user.email}), 200
    return jsonify({'error': "Forbidden"}), 403


@app.route("/reset_password", methods=['POST'], strict_slashes=False)
def get_reset_password_token():
    """
    POST /reset_password
    json object:
        - email
    Return:
        - 200: if email is registered
        - 403: if email not found
    """
    email = request.form.get('email')
    try:
        reset_token = auth.get_reset_password_token(email=email)
        return jsonify({"email": email, "reset_token": reset_token}), 200
    except ValueError:
        return 403


@app.route("/reset_password", methods=['PUT'], strict_slashes=False)
def update_password():
    """
    PUT /reset_password
    form object:
        - new_password
        - reset_token
        - email
    Return:
        - 200: if the user created
        - 403: when it fails
    """
    email = request.form.get('email')
    password = request.form.get('new_password')
    reset_token = request.form.get('request_token')

    try:
        auth.update_password(reset_token=reset_token, password=password)
        return jsonify({"email": email, "message": "Password updated"}), 200
    except ValueError:
        return 403


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
