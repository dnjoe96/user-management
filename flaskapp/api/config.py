import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '../.env'))


class Config(object):
    """ Config class to define application configurations and settings """
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'joseph'

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # to disable the feature of flasSQAlcheny that signals aplication each
    # time a change is made

    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')


class Development_config(Config):
    DEBUG = True
    SQLALCHEMY_ECHO = True


class Production_config(Config):
    DEBUG = False
