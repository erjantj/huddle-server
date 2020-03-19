import flask

from . import models
from . import errors
from . import jwt
from . import forms
from . import schemas
from . import auth_service

bp = flask.Blueprint('auth', __name__)

@bp.route('/me', methods=['GET'])
@forms.form_handler(response_schema=schemas.UserSchema())
def me():
    return auth_service.get_user()


@bp.route('/login', methods=['POST'])
def login():
    post_data = flask.request.get_json()

    user = models.User.query.filter_by(
        username=post_data.get('username')
      ).first()

    if not user:
        raise errors.InvalidUsernameOrPassword('Invalid username or password')

    auth_token = jwt.encode_auth_token(user.id)
    responseObject = {
        'status': 'success',
        'message': 'Successfully logged in.',
        'auth_token': auth_token.decode()
    }
    return flask.jsonify(responseObject)