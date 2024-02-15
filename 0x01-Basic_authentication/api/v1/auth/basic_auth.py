#!/usr/bin/env python3
"""basic_auth.py"""
from api.v1.auth.auth import Auth
import base64


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
