#!/usr/bin/env python3
"""auth module"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
import uuid


class AUTH:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

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

    def valid_login(self, email: str, password: str) -> bool:
        """check login
        arg:
            - email: email of the user
            - password: password of the user

        Retrun:
            - True: when the email and password matches
            - False: if they don't match
        """
        try:
            user = self._db.find_user_by(email=email)

            if bcrypt.checkpw(password.encode('utf-8'),
                              user.hashed_password):
                return True
            else:
                return False
        except NoResultFound:
            return False

    def _generate_uuid(self) -> str:
        """
            Generate uuid
            return:
                - uuid
        """
        return str(uuid.uuid4())

    def create_session(self, email: str) -> str:
        """
            Generate a session_Id
            args:
                - email
            Return:
                - session_Id
        """
        try:
            user = self._db.find_user_by(email=email)
            session_id = self._generate_uuid()
            self._db.update_user(user.id, session_id=session_id)

            return session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> User:
        """
            get user by session Id
            Return:
                - User: when found
                - None: not found
        """
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """
        Function that destroy the user id
        """
        try:
            self._db.find_user_by(id=user_id)
            self._db.update_user(user_id=user_id, session_Id=None)
            return None
        except NoResultFound:
            return None

    def get_reset_password_token(self, email: str) -> str:
        """
        Reset Password
        agrs:
            - email: the email needed to be reset
        Return:
            - the new reset_token if the user exist
            - ValueError: if the user doesn't exists
        """
        try:
            user = self._db.find_user_by(email=email)
            reset_token = self._generate_uuid()
            self._db.update_user(user_id=user.id, reset_token=reset_token)
            return reset_token
        except NoResultFound:
            raise ValueError

    def update_password(self, password: str, reset_token: str) -> None:
        """"
        Update Password
        args:
            - password: new password to be updated
            - reset_token: the user token
        Return:
            - None: if password is updated successful
        raises:
            - valueError: when the change password fails
        """
        # print(password)
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            # print("user found")
            hashed_password = self._hash_password(password)
            self._db.update_user(user_id=user.id,
                                 hashed_password=hashed_password,
                                 reset_token=None)
            return
        except NoResultFound:
            raise ValueError
