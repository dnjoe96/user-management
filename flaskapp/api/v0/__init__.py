from flask import  Blueprint
from flask import jsonify
# from api.v0.user import user_app
# from api.v0.errors import app_err


# create blueprint
app_views = Blueprint('app_views', __name__, url_prefix='/api/v0')

from api.v0.user.views import *

from api.v0.user import user_app
app_views.register_blueprint(user_app)

