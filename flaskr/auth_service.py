import flask

from . import errors
from . import jwt
from . import models


def get_user():
    auth_token = _get_auth_token()
    user_id = jwt.decode_auth_token(auth_token)
    user = models.User.query.filter_by(id=user_id).first()
    if not user:
        raise errors.UserNotFoundError()
    return user


def _get_auth_token():
    auth_header = flask.request.headers.get('Authorization')
    auth_token = ''
    if auth_header:
        auth_token = auth_header.split(" ")[1]
    return auth_token