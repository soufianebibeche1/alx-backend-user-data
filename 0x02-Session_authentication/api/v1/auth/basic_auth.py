#!/usr/bin/env python3
"""
Module for implementation of Basic authentication
"""
from api.v1.auth.auth import Auth
import base64
from models.user import User
from models.base import Base
from typing import TypeVar


class BasicAuth(Auth):
    """
    class that handles implementation of basic authentication
    """

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """
        extracts the authentication header and returns it
        """
        if authorization_header is None:
            return None
        if type(authorization_header) is not str:
            return None
        if authorization_header.startswith('Basic ') is False:
            return None
        else:
            token = authorization_header.split(' ')[1]
            return token

    def decode_base64_authorization_header(self,
                                           base64_authorization_header: str
                                           ) -> str:
        """
        decode the encoded authorization header value
        """
        if base64_authorization_header is None:
            return None
        if type(base64_authorization_header) is not str:
            return None
        try:
            decoded_token = base64.b64decode(base64_authorization_header,
                                             validate=True)
            return decoded_token.decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header: str
                                 ) -> (str, str):
        """
        extracts the user credentials from the base64decoded value
        """
        if decoded_base64_authorization_header is None:
            return (None, None)
        if type(decoded_base64_authorization_header) is not str:
            return (None, None)
        if ":" not in decoded_base64_authorization_header:
            return (None, None)
        user_details = decoded_base64_authorization_header.split(":")
        return tuple(user_details)

    def user_object_from_credentials(self, user_email: str,
                                     user_pwd: str
                                     ) -> TypeVar('User'):
        """
        get a user from the file storage using the user credentials
        """
        if user_email is None or type(user_email) is not str:
            return None
        if user_pwd is None or type(user_pwd) is not str:
            return None

        user_instances = User.search(attributes={"email": user_email})
        if len(user_instances) == 0:
            return None
        if user_instances[0].is_valid_password(user_pwd) is False:
            return None
        return user_instances[0]

    def current_user(self, request=None) -> TypeVar('User'):
        """
        method that overloads auth and retrieves the user instance for a
        request
        """
        if request is None:
            return None
        auth_header = super().authorization_header(request)
        if auth_header is not None:
            auth_token = self.extract_base64_authorization_header(auth_header)
        else:
            return None
        decoded_token = self.decode_base64_authorization_header(auth_token)
        if decoded_token is not None:
            user_credentials = self.extract_user_credentials(decoded_token)
        else:
            return None

        user_email, user_pwd = user_credentials

        user = self.user_object_from_credentials(user_email, user_pwd)
        if user:
            return user
        else:
            return None
