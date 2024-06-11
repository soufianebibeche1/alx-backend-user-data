#!/usr/bin/env python3
"""
A flask application
"""
from flask import Flask, jsonify, make_response, request, abort, redirect
from auth import Auth


AUTH = Auth()
app = Flask(__name__)


@app.route('/', methods=['GET'], strict_slashes=False)
def index():
    """
    index page of the application
    """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def users():
    """
    endpoint to register a new user
    """
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        new_user = AUTH.register_user(email, password)
        if new_user:
            return jsonify({"email": new_user.email,
                           "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login():
    """
    logs a user in and creates a session
    """
    email = request.form.get("email")
    if not email:
        abort(401)
    password = request.form.get("password")
    if not password:
        abort(401)
    if AUTH.valid_login(email, password):
        user_session_id = AUTH.create_session(email)
        if user_session_id:
            response = jsonify({"email": email, "message": "logged in"})
            response.set_cookie("session_id", user_session_id)
            return response
        abort(401)
    abort(401)


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout():
    """
    view function to handle log out
    """
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        AUTH.destroy_session(user.id)
        return redirect('/')
    return make_response(), 403


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile():
    """
    implement a user profile
    """
    session_id = request.cookies.get('session_id')
    if not session_id:
        abort(403)
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        return make_response(jsonify({"email": user.email})), 200
    abort(403)


@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def get_reset_password_token():
    """
    route to implement getting a password reset token
    """
    try:
        email = request.form.get('email')
        reset_token = AUTH.get_reset_password_token(email)
        return make_response(jsonify({"email": email,
                                     "reset_token": reset_token})), 200
    except ValueError:
        abort(403)


@app.route('/reset_password', methods=['PUT'], strict_slashes=False)
def update_password():
    """
    update a user password
    """
    try:
        email = request.form.get('email')
        reset_token = request.form.get('reset_token')
        new_password = request.form.get('new_password')
        AUTH.update_password(reset_token, new_password)
        return make_response({"email": email,
                             "message": "Password updated"}), 200
    except ValueError:
        abort(403)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000', debug=True)
