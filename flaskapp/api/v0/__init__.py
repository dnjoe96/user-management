from flask import  Blueprint
from flask import jsonify
from api.v0.user import user_app
from api.v0.error import app_err


# create blueprint
app_views = Blueprint('app_views', __name__, url_prefix='/api/v0')

# register blue print for new apps created
app_views.register_blueprint(user_app)
# app_views.register_blueprint(app_err)


@app_views.route('/')
def v0_index():
    return jsonify({'message': 'welcome to /api/v0 root API'})

