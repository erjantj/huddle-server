"""JWT token handlers."""

import datetime
from flask import current_app
import jwt

from flaskr import errors


def encode_auth_token(user_id: int) -> str:
    """Generates the Auth Token.

    Args:
      user_id: A user id.

    Returns:
      Encoded auth token.

    Raises:
      errors.EncodingTokenError: If unable to encode token payload.
    """

    jwt_ttl = current_app.config.get('JWT_TTL')
    secret_key = current_app.config.get('SECRET_KEY')
    algorithm = 'HS256'
    now = datetime.datetime.utcnow()

    try:
        payload = {
            'exp': now + datetime.timedelta(seconds=jwt_ttl),
            'iat': now,
            'sub': user_id
        }
        return jwt.encode(payload, secret_key, algorithm=algorithm)
    except Exception:
        raise errors.EncodingTokenError()


def decode_auth_token(auth_token: str) -> int:
    """Decodes the auth token

    Args:
      auth_token: An authentication token.

    Returns:
      Decoded user id.

    Raises:
      errors.ExpiredSignatureError: If auth token is expired.
      errrors.InvalidTokenError: If auth token is malformed.
    """
    try:
        payload = jwt.decode(auth_token, current_app.config.get('SECRET_KEY'))
        return payload['sub']
    except jwt.ExpiredSignatureError:
        raise errors.ExpiredSignatureError()
    except jwt.InvalidTokenError:
        raise errors.InvalidTokenError()
