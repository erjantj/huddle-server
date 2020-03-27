"""Module that contains authentication logic and helpers."""
import functools

import flask

from flaskr import errors
from flaskr import jwt
from flaskr import models


def get_user():
    """Returns authenticated user.

    Raises:
        error.UserNotFoundError: If user is not found or
        token is not valid.

    Returns:
        The authenticated user.
    """
    auth_token = _get_auth_token()
    user_id = jwt.decode_auth_token(auth_token)
    user = models.User.query.filter_by(id=user_id).first()
    if not user:
        raise errors.UserNotFoundError()
    return user


def _get_auth_token():
    """Returns auth token retrived from request header.

    Returns:
        Auth token.
    """
    auth_header = flask.request.headers.get('Authorization')
    auth_token = ''
    if auth_header:
        auth_token = auth_header.split(" ")[1]
    return auth_token


def login_required(func):
    """Annotation to check user authentication."""
    @functools.wraps(func)
    def decorated_view(*args, **kwargs):
        try:
            get_user()
        except errors.BaseError:
            raise errors.UnauthorizedError()
        return func(*args, **kwargs)
    return decorated_view
