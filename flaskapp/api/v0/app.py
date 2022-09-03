#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from typing import Tuple

# from api.v0.user.views import app_views
from flask import Flask, jsonify, abort, request, Response
import flask_cors
import os
from api.v0 import app_views
from api.v0.error import app_err


app = Flask(__name__)
app.register_blueprint(app_views)
app.register_blueprint(app_err)

flask_cors.CORS(app, resources={r"/api/v0/*": {"origins": "*"}})
auth = os.environ.get('AUTH_TYPE', None)

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


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port, debug=True)
