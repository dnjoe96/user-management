#!/usr/bin/env python3
""" User Schema Module"""

from api.v0.app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import bcrypt


class User(db.Model):
    """ User class """
    __tablename__ = 'user'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.String(100), nullable=False, primary_key=True)
    username = db.Column(db.String(25), nullable=False, unique=True)
    firstname = db.Column(db.String(25), nullable=False)
    lastname = db.Column(db.String(25), nullable=False)
    middlename = db.Column(db.String(25), nullable=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    phone = db.Column(db.String(15), nullable=True)
    city = db.Column(db.String(25), nullable=True)
    state = db.Column(db.String(50), nullable=True)
    country = db.Column(db.String(250), nullable=True)
    group = db.Column(db.String(25), nullable=True)
    active = db.Column(db.String(25), nullable=False, default=0)
    rank = db.Column(db.String(20), nullable=True)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    date_updated = db.Column(db.DateTime, nullable=True)
    activation_token = db.Column(db.String(20), nullable=True)
    deletion_flag = db.Column(db.String(2), nullable=True)

    def __repr__(self):
        """ Class object representation """
        return '<User(id=\'%s\', email=\'%s\')>' % (
            self.id, self.email
        )

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    # def colomns(self):
    #     keys = [one for one in User.__dict__.keys() if one[:2] == '__']
    #     return keys


class Credentials(db.Model):
    __tablename__ = 'credentials'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, nullable=False, autoincrement=True, primary_key=True)
    user_id = db.Column(db.String(100), db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('user', uselist=False))
    password = db.Column(db.String(200), nullable=False)
    date_updated = db.Column(db.DateTime, nullable=True)

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def set_password(self, password: str) -> None:
        """ Function to hash password with salt and return
        byte string password """
        passwrd = password.encode()
        self.password = bcrypt.hashpw(passwrd, bcrypt.gensalt()).decode()

    def check_password(self, raw_password: str) -> bool:
        """ Function to validate if password matches a hashed password """
        if bcrypt.checkpw(raw_password.encode('utf-8'), self.password.encode()):
            return True
        else:
            return False


class Session(db.Model):
    __tablename__ = 'sessions'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, nullable=False, autoincrement=True, primary_key=True)
    user_id = db.Column(db.String(100), db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('token', uselist=False))
    token = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, nullable=True)

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
