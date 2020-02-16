import flask
from . import errors

bp = flask.Blueprint('error_handlers', __name__)

@bp.app_errorhandler(errors.BaseError)
def handle_base_error(error):
    response = flask.jsonify(error.to_dict())
    response.status_code = error.status_code
    return response
