from flask import  Blueprint

app_err = Blueprint('errors', __name__)

from . import handlers
