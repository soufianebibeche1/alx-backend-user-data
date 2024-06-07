#!/usr/bin/env python3
"""
Module for handling the user authentication
"""
from flask import request
from typing import List, TypeVar
import os


_my_session_id = os.getenv('SESSION_NAME')


class Auth:
    """
    class for handling authentication
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        checks if the path requuires a user authentication or not
        """
        if path is None:
            return True

        if excluded_paths is None or len(excluded_paths) == 0:
            return True

        if path.endswith('/'):
            if path in excluded_paths:
                return False
            else:
                return True
        else:
            path = path + ('/')
            if path in excluded_paths:
                return False
            else:
                return True

    def authorization_header(self, request=None) -> str:
        """
        returns None
        """
        if request is None:
            return None
        if request.headers.get('Authorization') is None:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """
        returns None
        """
        return None

    def session_cookie(self, request=None):
        """
        returns a cookie value from a request
        """
        if request is None:
            return None
        return request.cookies.get(_my_session_id)
