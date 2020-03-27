"""Auth api handlers."""
import flask

from flaskr import models
from flaskr import errors
from flaskr import jwt
from flaskr import forms
from flaskr import schemas
from flaskr import auth_service

# pylint: disable=invalid-name
bp = flask.Blueprint('auth', __name__)


@bp.route('/me', methods=['GET'])
@forms.form_handler(response_schema=schemas.UserSchema())
def me():
    """Returns curent user if authorized."""
    return auth_service.get_user()


@bp.route('/login', methods=['POST'])
def login():
    """Login endpoint handler."""
    post_data = flask.request.get_json()

    user = models.User.query.filter_by(
        username=post_data.get('username')
    ).first()

    if not user:
        raise errors.InvalidUsernameOrPasswordError(
            'Invalid username or password')

    auth_token = jwt.encode_auth_token(user.id)
    responseObject = {
        'status': 'success',
        'message': 'Successfully logged in.',
        'auth_token': auth_token.decode()
    }
    return flask.jsonify(responseObject)
