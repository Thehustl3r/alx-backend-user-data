#!/usr/bin/env python3
"""The module for auth"""
from flask import request
from typing import List, TypeVar


class Auth:
    """The class to hold all the authentication"""

    def require_auth(self, path: str, excluded_path: List[str]) -> bool:
        """The function that will check if the auth is required"""

        if path is None or excluded_path is None:
            return True
        if not path.endswith('/'):
            path += '/'
        if path in excluded_path:
            return False

        return True

    def authorization_header(self, request=None) -> str:
        """the function"""
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Function the user """
        return None
