#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from typing import Tuple

from flask import Flask, jsonify, abort, request, Response
from flask_sqlalchemy import SQLAlchemy
import flask_cors
from flask_migrate import Migrate
import os


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Postgres12@soft-dev.cixnnif6iavq.us-east-1.rds.amazonaws.com/softdev01'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'secret'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

flask_cors.CORS(app, resources={r"/api/v0/*": {"origins": "*"}})
auth = os.environ.get('AUTH_TYPE', None)


from api.v0.errors import app_err
app.register_blueprint(app_err)

from api.v0 import app_views
# from api.v0.user import user_app
app.register_blueprint(app_views)

# if auth:
#     if auth == 'basic_auth':
#         from api.v1.auth.basic_auth import BasicAuth
#         auth = BasicAuth()
#     else:
#         from api.v1.auth.auth import Auth
#         auth = Auth()


@app.before_request
def just_before_request():
    """ Function implements before every request """
    dlist = ['/api/v1/status/', '/api/v1/unauthorized/', '/api/v1/forbidden/']
    if auth:
        if auth.require_auth(request.path, dlist):
            if not auth.authorization_header(request):
                abort(401)
            if not auth.current_user(request):
                abort(403)
            request.currrent_user = auth.current_user


@app.route('/')
def index():
    return jsonify({'message': 'welcome to the root of this API'})


@app.route('/api/v0')
def v0_index():
    return jsonify({'message': 'welcome to /api/v0 root API'})


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port, debug=True)
