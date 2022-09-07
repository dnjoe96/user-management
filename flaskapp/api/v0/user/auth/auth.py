#!/usr/bin/env python3
""" Module for Auth """
import bcrypt
from user import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4


def _hash_password(password: str) -> bytes:
    """ The function hashes a password """
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(bytes(password.encode('utf-8')), salt)


def _generate_uuid() -> str:
    """ Generate uuid """
    return str(uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """ constructor method"""
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """ This method is used to register a user"""
        try:
            self._db.find_user_by(email=email)
            raise ValueError('<user\'s email> already exists>')
        except NoResultFound:
            password = _hash_password(password).decode('utf-8')
            return self._db.add_user(email=email, hashed_password=password)

    def valid_login(self, email: str, password: str) -> bool:
        """ Check if a user is valid """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False

        return bcrypt.checkpw(password.encode('utf-8'),
                              user.hashed_password.encode('utf-8'))

    def create_session(self, email: str) -> str:
        """ Create session id"""
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None
        session_id = _generate_uuid()
        self._db.update_user(user_id=user.id, session_id=session_id)
        return session_id

    def get_user_from_session_id(self, session_id: str):
        """ Get a user from session_id """
        if not session_id:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None
        return user

    def destroy_session(self, user_id: str):
        """ Function to destroy session """
        try:
            self._db.update_user(user_id, session_id=None)
        except Exception:
            return None