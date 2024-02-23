#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.session import Session

from user import Base
from user import User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Add the user to the database"""

        new_user = User(email=email, hashed_password=hashed_password)
        # new_user.email = email
        # new_user.hashed_password = hashed_password
        self._session.add(new_user)

        self._session.commit()
        # self._session.close(ls)

        return new_user

    def find_user_by(self, **kwargs) -> User:
        """Find a user in the database using arbitary keyword arguments.
        Returns:
            the first User object found matching the query

        Raises:
            NoResultFound: If no matching user is found.
            InvalidRequestError: If invalid query arguments are passed.
        """
        try:
            user = self._session.query(User).filter_by(**kwargs).first()
            if not user:
                raise NoResultFound("No useer")
            return user
        except NoResultFound as e:
            raise e
        except InvalidRequestError:
            raise InvalidRequestError