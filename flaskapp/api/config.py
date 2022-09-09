# the essense of creating a configuration setting app seperately
# from the other files or the file that was used to create application
# is for the pirpose of simplicity. and best practice.


# so we import os
import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '../.env'))


# creating a configuration class
class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'joseph'

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI')
    # SQLALCHEMY_DATABASE_URI = 'mysql://user1:Praise@1234@localhost/microblog'
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # to disable the feature of flasSQAlcheny that signals apllication each time a change is made

    # ELASTICSEARCH_URL = os.environ.get('ELASTICSEARCH_URL')
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')


class Development_config(Config):
    DEBUG = True
    SQLALCHEMY_ECHO = True


class Production_config(Config):
    DEBUG = False
