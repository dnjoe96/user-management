from flask import  Blueprint

app_err = Blueprint('error', __name__)

from .handlers import *
