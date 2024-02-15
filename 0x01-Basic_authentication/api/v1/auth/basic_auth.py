#!/usr/bin/env python3
"""basic_auth.py"""
from api.v1.auth.auth import Auth
from typing import TypeVar
import base64
from models.user import User


class BasicAuth(Auth):
    """A basic clasll of the authentication"""

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """This function that extract only base64 part
        Return:
            - the base64 part of the Authorization header
        """
        if authorization_header is None or not \
                isinstance(authorization_header, str):
            return None

        if not authorization_header.startswith('Basic '):
            return None

        return authorization_header.split(" ")[1]

    def decode_base64_authorization_header(self,
                                           base64_authorization_header: str
                                           ) -> str:
        """
        Function that decodes the base64
        Return:
            - the decode value extracted from the header
        """
        undecoded_value = base64_authorization_header
        if undecoded_value is None or \
                not isinstance(undecoded_value, str):
            return None
        try:
            decoded_bytes = base64.b64decode(undecoded_value)
            decoded_string = decoded_bytes.decode('utf-8')
            return decoded_string
        except Exception as e:
            return None

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header: str
                                 ) -> (str, str):
        """
        The Function that extract the user_credential from the header
        Return:
            - User credetials
        """
        if decoded_base64_authorization_header is None or \
                not isinstance(decoded_base64_authorization_header, str):
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None

        return decoded_base64_authorization_header.split(':')

    def user_object_from_credentials(self,
                                     user_email: str,
                                     user_pwd: str
                                     ) -> TypeVar('User'):
        """
        The Function that converts that  user object based on credentials
        Return:
            - user object
        """
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None
        user = User.search({"email": user_email})

        if not user:
            return None
        if user[0].is_valid_password(user_pwd):
            return user[0]
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Function that will retriev the user from the database
        Return:
            - the user if exist
            - or raise an error
        """
        header = self.authorization_header(request)
        undecoded_header = self.extract_base64_authorization_header(header)
        decoded_header = self.decode_base64_authorization_header(
            undecoded_header)
        user_email, user_pwd = self.extract_user_credentials(decoded_header)
        return self.user_object_from_credentials(user_email, user_pwd)
