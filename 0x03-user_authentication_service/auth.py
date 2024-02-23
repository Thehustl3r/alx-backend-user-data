#!/usr/bin/env python3
"""auth module"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        Register a new user.
        Args:
            email(str): the email of the user.
            password (str): The password of the User.

        Returns:
            User: The newly registered user Object.

        Raise:
            ValueError: If a user already exists with the provided email
        """
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            pass

        hashed_password = self._hash_password(password)

        new_user = self._db.add_user(
            email=email, hashed_password=hashed_password)
        return new_user

    def _hash_password(self, password: str) -> bytes:
        """
        creat a hash password form the string
        arg:
            - password - as string
        Return:
            - The hashed password
        """
        salt = bcrypt.gensalt()

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed_password
