#!/usr/bin/env python3
"""basic_auth.py"""
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """A basic clasll of the authentication"""

    def extract_base64_authorization_header(self, authorization_header: str) -> str:
        """This function that extract only base64 part
        Return:
            - the base64 part of the Authorization header
        """
        if authorization_header is None or not isinstance(authorization_header, str):
            return None

        if not authorization_header.startswith('Basic '):
            return None

        return authorization_header.split(" ")[1]
