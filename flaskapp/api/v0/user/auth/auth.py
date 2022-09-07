#!/usr/bin/env python3
""" Authentication Module """
from flask import request
from typing import List, TypeVar


class Auth:
    """
    Auth class
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ function to determine path that require auth
        """
        if not path or not excluded_paths:
            return True
        path = path + '/' if path[-1] != '/' else path
        if len(excluded_paths) == 0:
            return True
        if path in excluded_paths:
            return False
        return True

    def authorization_header(self, request=None) -> str:
        """ Generates auth header"""
        if not request:
            return None
        if not request.headers.get('Authorization'):
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """ Function to return current user"""
        return None
