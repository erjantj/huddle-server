"""Handles application errors."""
import flask
from flaskr import errors

# pylint: disable=invalid-name
bp = flask.Blueprint('error_handlers', __name__)


@bp.app_errorhandler(errors.BaseError)
def handle_base_error(error):
    """Handles application's error response."""
    response = flask.jsonify(error.to_dict())
    response.status_code = error.status_code
    return response
