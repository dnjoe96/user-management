from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.session import Session
from typing import Callable
from api.v0.user.models import User, Session, Credentials
from api.v0.app import db


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        return db.session

    def add_user(self, email: str, hashed_password: str) -> User:
        """ Method to add a new user """
        user = User(id=1, email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()
        return user

    # @staticmethod
    def find_user_by(self, **vals) -> User:
        """ find a user by an arbitrary attribute """
        try:
            user = self._session.query(User).filter_by(**vals).first()
        except TypeError:
            raise InvalidRequestError
        if user is None:
            raise NoResultFound
        return user

    def update_user(self, user_id: int, **vars) -> None:
        """ method to update a user and save in db"""
        try:
            user = self.find_user_by(id=user_id)
            for key, value in vars.items():
                setattr(user, key, value)
        except Exception:
            raise Exception

        self._session.commit()
        return None