#!/usr/bin/env python3
"""basic_auth.py"""
from api.v1.auth.auth import Auth
from typing import TypeVar
import base64
from models.user import User
import uuid
import os


class SessionAuth(Auth):
    """A class that handles session authentication"""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """Function that creates new session for the user"""
        if user_id is None or not isinstance(user_id, str):
            return None

        sessionId = str(uuid.uuid4())
        self.user_id_by_session_id[sessionId] = user_id
        return sessionId

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Function that check for the session id
        Return:
            - user_id if the session_id is valid
            - otherwise None
        """
        if session_id is None or not isinstance(session_id, str):
            return None

        user_id = self.user_id_by_session_id.get(session_id)
        return user_id
