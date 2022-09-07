#!/usr/bin/env python3
""" User Schema Module"""
from flask_sqlalchemy import Model
from sqlalchemy.ext.declarative import declarative_base
from api.v0.app import db


class User(db.Model):
    """ User class """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(250), nullable=False)
    hashed_password = db.Column(db.String(250), nullable=False)
    session_id = db.Column(db.String(250), nullable=True)
    reset_token = db.Column(db.String(250), nullable=True)

    def __repr__(self):
        """ Class object representation """
        return '<User(id=\'%s\', email=\'%s\')>' % (
            self.id, self.email
        )


class Credentials(db.Model):
    __tablename__ = 'credentials'
    pass
