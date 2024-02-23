#!/usr/bin/env python3
"""app module"""
from flask import Flask, jsonify, request
from auth import Auth


app = Flask(__name__)
auth = Auth()


@app.route("/", methods=['GET'], strict_slashes=False)
def welcome():
    """the welcome message"""
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=['POST'], strict_slashes=False)
def register_user():
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
