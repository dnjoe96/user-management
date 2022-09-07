#!/usr/bin/env python3
""" Authentication Module """
from api.v1.auth.auth import Auth
from flask import request
from typing import List, TypeVar
import base64
from models.user import User


class BasicAuth(Auth):
    """
    Basic Auth class
    """
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """ The function extracts the endocded string from the header"""
        if not authorization_header:
            return None
        if type(authorization_header) is not str:
            return None
        if authorization_header[:6] != 'Basic ':
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(self, base64_authorization_header: str) -> str:
        """ The function decodes the Authorization in header """
        if not base64_authorization_header:
            return None
        if type(base64_authorization_header) is not str:
            return None
        try:
            string = base64_authorization_header.encode('utf-8')
            dcode = base64.decodebytes(string)
        except Exception:
            return None
        return dcode.decode()

    def extract_user_credentials(self, decoded_base64_authorization_header: str) -> (str, str):
        """ Extract user detail from auth header """
        if decoded_base64_authorization_header is None:
            return None, None
        if type(decoded_base64_authorization_header) is not str:
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None
        email = decoded_base64_authorization_header.split(':')[0]
        pwd = ''.join(decoded_base64_authorization_header.split(':')[1:])
        return email, pwd

    def user_object_from_credentials(self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """ The function get user objects from"""
        if not user_email or not user_pwd:
            return None
        if type(user_email) is not str or type(user_pwd) is not str:
            return None
        try:
            users = User.search({'email': user_email})
        except Exception:
            return None
        for user in users:
            if user.is_valid_password(user_pwd):
                return user
        return None
