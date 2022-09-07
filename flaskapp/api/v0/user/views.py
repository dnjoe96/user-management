from . import user_app
from flask import jsonify


@user_app.route('/')
def user_index():
    return jsonify({'message': 'welcome to the root of the user API'})


@user_app.route('/login', methods=['POST'])
def login():
    return 'not implemented'


@user_app.route('/logout', methods=['DELETE'])
def logout():
    return 'not implemented'


@user_app.route('/register', methods=['POST'], strict_slashes=False)
def register():
    return 'not implemented'


@user_app.route('/profile/<username>', methods=["GET"], strict_slashes=False)
def profile(username):
    return 'not implemented'


@user_app.route('/edit/<username>')
def edit_profile(username):
    return 'not implemented'


@user_app.route('/activate')
def activate_user():
    return 'not implemented'


@user_app.route('/deactivate')
def deactivate_user():
    return 'not implemented'


@user_app.route('/role', methods=['POST'])
def add_role():
    return 'not implemented'


@user_app.route('/role', methods=['GET'])
def get_roles():
    return 'not implemented'
