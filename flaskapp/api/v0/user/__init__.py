from flask import Blueprint

# user = Blueprint('user', __name__, url_prefix='/api/v0/user')
user_app = Blueprint('user_app', __name__, url_prefix='/api/v0/user')

from . import views
