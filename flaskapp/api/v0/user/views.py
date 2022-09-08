import random

import sqlalchemy.exc
from flask import jsonify, request, redirect, url_for, abort
from . import user_app
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from api.v0.app import db, app
from uuid import uuid4
from datetime import datetime, timedelta
from api.v0.user.models.db import User, Credentials, Session


@user_app.route('/')
def user_index():
    return jsonify({'message': 'welcome to the root of the user API'})


@user_app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')

    user = User.query.filter_by(username=username).first()
    print(user.username)
    if not user:
        abort(401, {"message": "user not found"})

    cred = Credentials.query.filter_by(user_id=user.id).first()
    if not password:
        return jsonify({'status': 'false', 'message': 'no credential found for this user'}), 401

    if cred.check_password(password):
        session_id = uuid4()
        session = Session(user_id=user.id, token=session_id, date_created=datetime.utcnow())

        # generates the JWT Token
        payload = {
            'id': user.id,
            'exp': datetime.utcnow() + timedelta(minutes=30)
        }

        token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm="HS256")
        print(token)
        resp = jsonify({
            'status': 'ok',
            'message': f"{user.username} logged in successful",
            'session_id': session_id,
            'token': token
        })
        db.session.add(session)
        db.session.commit()
        resp.set_cookie(str(session_id))
        return resp, 200

    return jsonify({'message': 'password incorrect'}), 403


@user_app.route('/logout', methods=['DELETE'])
def logout():
    """ Logout view """
    # session_id = request.cookies.get('session_id')
    # if session_id:
    #     user = AUTH.get_user_from_session_id(session_id)
    #     if user:
    #         AUTH.destroy_session(user.id)
    #         return redirect(url_for('index'))
    # abort(403)


@user_app.route('/register', methods=['POST'], strict_slashes=False)
def register():
    data = request.get_json()

    fields = [one for one in User.__dict__.keys() if one[0] != '_']
    for one in data.keys():
        if one not in fields and one != 'password':
            return jsonify({'status': 'false', 'message': f"{one} is not a valid field"}), 403

    for one in ['firstname', 'lastname', 'username', 'email', 'password']:
       if one not in data.keys():
           return jsonify({'status': 'false', 'message': 'firstname, lastname, email, password is required'}), 403

    data['id'] = str(uuid4())
    data['activation_token'] = random.randint(0, 10000)
    cred = Credentials(
        user_id=data['id'],
        date_updated=datetime.utcnow()
    )
    cred.set_password(data['password'])
    print(data)
    data.pop('password')
    user = User(**data)
    db.session.add(user)
    db.session.add(cred)
    try:
        db.session.commit()
    except sqlalchemy.exc.IntegrityError as e:
        db.session.rollback()
        return jsonify({'status': 'false', 'message': 'record already exists'}), 403

    return jsonify({
        'status': 'true',
        'message': f"User {data['username']} has been created",
        'user_id': data['id'],
        'activation_token': data['activation_token']
    }), 201


@user_app.route('/profile/<username>', methods=["GET"], strict_slashes=False)
def profile(username):

    return 'not implemented'


@user_app.route('/edit/<username>')
def edit_profile(username):
    return 'not implemented'


@user_app.route('/activate/<user_id>/<token>', methods=['GET'], strict_slashes=False)
def activate_user(user_id, token):
    if not user_id and not token:
        return jsonify({'status': 'false', 'message': 'invalid activation string. contact admin'}), 403
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return jsonify({'status': 'false', 'message': 'This use does not exist'}), 403
    if user.active == 1:
        return jsonify({'status': 'false', 'message': 'Invalid Operation'}), 403
    if user.activation_token != token:
        return jsonify({'status': 'false', 'message': 'Invalid token'}), 403
    user.active = 1
    user.activation_token = ''
    db.session.commit()
    return jsonify({'status': 'true', 'message': f"User {user.username} is activated. Congratulations!!"}), 200


@user_app.route('/deactivate', methods=['PUT'], strict_slashes=False)
def deactivate_user():
    data = request.json.get('username')
    user = User.query.filer_by(username=data)
    user.active = 0
    db.session.commit()

    # find user session in Session table and delete session.
    return jsonify({'status': 'true', 'message': f'user {data} deactivated successfully'}), 200


@user_app.route('/role', methods=['POST'])
def add_role():
    return 'not implemented'


@user_app.route('/role', methods=['GET'])
def get_roles():
    return 'not implemented'


@user_app.route('/all', methods=['GET'], strict_slashes=False)
def all_user():
    data = request.json.get('limit')
    print(data)
    try:
        users = [user.to_dict() for user in User.query.limit(data).all()]
    except sqlalchemy.exc as e:
        return jsonify({'status': 'false', 'message': 'Something went wrong'})
    return jsonify({'status': 'true', 'users': users})