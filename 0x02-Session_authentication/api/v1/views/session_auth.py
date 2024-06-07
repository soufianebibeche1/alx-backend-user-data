#!/usr/bin/env python3
"""
Module that handles all routes for the session authentication
"""

from flask import request, jsonify, make_response
from api.v1.views import app_views
from models.user import User
import os


@app_views.route('auth_session/login',
                 methods=['POST'], strict_slashes=False)
def session_auth():
    """
    method that creates the route for session authentication
    """
    # get the email and password
    email = request.form.get('email')
    if not email:
        return make_response(jsonify({"error": "email missing"})), 400
    password = request.form.get('password')
    if not password:
        return make_response(jsonify({"error": "password missing"})), 400
    # retrieve user from database using email
    user_instances = User.search({"email": email})
    if len(user_instances) == 0:
        message = {"error": "no user found for this email"}
        return make_response(jsonify(message)), 404
    user = user_instances[0]
    if not user.is_valid_password(password):
        return make_response(jsonify({"error": "wrong password"})), 401

    from api.v1.app import auth

    new_session = auth.create_session(user.id)
    response = jsonify(user.to_json())
    response.set_cookie(os.getenv('SESSION_NAME'), new_session)
    return response


@app_views.route('auth_session/logout', methods=['DELETE'],
                 strict_slashes=False)
def delete_session():
    """
    deletes the session and logs out the user
    """
    from api.v1.app import auth
    if auth.destroy_session(request) is False:
        abort(404)
    return make_response(jsonify({})), 200
