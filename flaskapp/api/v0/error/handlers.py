from flask import jsonify, Response
from . import app_err


@app_err.errorhandler(404)
def not_found(error) -> tuple[Response, int]:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


@app_err.errorhandler(401)
def unauthorized(error) -> tuple[Response, int]:
    """ Error handler for Unauthorised
    """
    return jsonify({"error": "Unauthorized"}), 401


@app_err.errorhandler(403)
def forbidden(error) -> tuple[Response, int]:
    """ Error handler for Forbidden
    """
    return jsonify({"error": "Forbidden"}), 403
