import random
from functools import wraps
import sqlalchemy.exc
from flask import jsonify, request, redirect, url_for, abort
from api.v0.user import user_app
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from api.v0.app import db, app
from uuid import uuid4
from datetime import datetime, timedelta
from api.v0.user.models.user_model import User, Credentials, Session


# @user_app.route('/')
# def user_index():
#     return jsonify({'message': 'welcome to the root of the user API'})

@app.route('/api/v0/user', methods=['GET'], strict_slashes=False)
def user_index():
    return jsonify({'status': 'true', 'message': 'welcome to the user api'}), 200


def auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # jwt is passed in the request header
        # print(request.headers)
        if 'authentication' in request.headers:
            sessionid = request.headers['authentication']
        else:
            return jsonify({'message': 'You need to be logged in'}), 401
        print(sessionid)
        try:
            session = Session.query.filter_by(token=sessionid).first()
            if session:
                current_user = User.query.filter_by(id=session.user_id).first()
            else:
                return jsonify({'message': 'You need to be logged in'}), 401
        except Exception as e:
            print(f'{e.__class__} - {str(e)} - {e}')
            return jsonify({
                'message': 'Login Invalid'
            }), 401
        # returns the current logged in users contex to the routes
        return f(current_user.to_dict(), *args, **kwargs)

    return decorated


@app.route('/api/v0/user/login', methods=['POST'], strict_slashes=False)
def login():
    username = request.json.get('username')
    password = request.json.get('password')

    user = User.query.filter_by(username=username).first()

    if not user:
        return jsonify({"message": "user not found or user inactive"}), 403
    print(user.active)
    if user.active == '0':
        return jsonify({'status': 'false', 'message': 'user is not active'}), 403

    cred = Credentials.query.filter_by(user_id=user.id).first()
    if not password:
        return jsonify({'status': 'false', 'message': 'no credential found for this user'}), 401

    # if cred.check_password(password):
    if not cred.check_password(password):
        return jsonify({'status': 'false', 'message': 'password incorrect'}), 403

    session = Session.query.filter_by(user_id=user.id).first()
    print(session)
    if session:
        return jsonify({'status': 'false', 'message': 'you are already logged in', 'session_id': session.token}), 200
    session_id = uuid4()
    session = Session(user_id=user.id, token=session_id, date_created=datetime.utcnow())

    resp = jsonify({
        'status': 'true',
        'message': f"{user.username} logged in successful",
        'session_id': session_id
    })
    db.session.add(session)
    db.session.commit()
    resp.set_cookie(str(session_id))
    return resp, 200


@app.route('/api/v0/user/logout', methods=['DELETE'])
@auth_required
def logout(current_user):
    """ Logout view """

    session = Session.query.filter_by(user_id=current_user['id']).first()
    print(session)
    if session:

        db.session.delete(session)
        db.session.commit()
        # resp.set_cookie(str(session_id))
        return jsonify({'status': 'true', 'message': 'you are logged out, bye'}), 200
    return jsonify({'status': 'false', 'message': 'You are not logged in'}), 400


@app.route('/api/v0/user/register', methods=['POST'], strict_slashes=False)
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


@app.route('/api/v0/user/profile/<username>', methods=["GET"], strict_slashes=False)
@auth_required
def profile(current_user, username):
    print(current_user)
    if current_user['username'] != username:
        return jsonify({'status': 'false', 'message': 'Unauthorised user'}), 401
    return jsonify({'status': 'true', 'user': current_user})


@app.route('/api/v0/user/edit/<username>', methods=['PUT'], strict_slashes=False)
def edit_profile(username):
    data = request.get_json()

    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({'status': 'false', 'message': "User does not exit"}), 404
    if user.active == '0':
        return jsonify({'status': 'false', 'message': "User is not active.Activate user or contact admin"}), 400

    fields = [one for one in User.__dict__.keys() if one[0] != '_']
    for one in data.keys():
        if one not in fields or one == 'username':
            return jsonify({'status': 'false', 'message': f"{one} is not a valid field"}), 403

    User.query.filter_by(username=username).update(data)

    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        return jsonify({'status': 'false', 'message': 'something went wrong'}), 403

    return jsonify({
        'status': 'true',
        'message': 'record updated'
    }), 201


@app.route('/api/v0/user/activate/<user_id>/<token>', methods=['GET'], strict_slashes=False)
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


@app.route('/api/v0/user/deactivate', methods=['PUT'], strict_slashes=False)
def deactivate_user():
    data = request.json.get('username')

    user = User.query.filter_by(username=data).first()
    print(user)
    if user:
        user.active = 0
        db.session.commit()
        return jsonify({'status': 'true', 'message': f'user {data} deactivated successfully'}), 200
    return jsonify({'status': 'true', 'message': f'user not found'}), 200


@app.route('/api/v0/user/role', methods=['POST'])
def add_role():
    return 'not implemented'


@app.route('/api/v0/user/role', methods=['GET'])
def get_roles():
    return 'not implemented'


@app.route('/api/v0/user/all', methods=['GET'], strict_slashes=False)
def all_user():
    data = request.json.get('limit')
    print(data)
    try:
        users = [user.to_dict() for user in User.query.limit(data).all()]
    except sqlalchemy.exc:
        return jsonify({'status': 'false', 'message': 'Something went wrong'})
    return jsonify({'status': 'true', 'users': users})


@app.route('/api/v0/user/verification', methods=['GET'], strict_slashes=False)
def verification():
    """ Verify is you are authentication
    """
    return 'Not implemented'
