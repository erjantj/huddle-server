from flask import current_app
import datetime
import jwt

from . import errors

def encode_auth_token(user_id):
    """
    Generates the Auth Token
    :return: string
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
    except Exception as e:
        return e


def decode_auth_token(auth_token):
    """
    Decodes the auth token
    :param auth_token:
    :return: integer|string
    """
    try:
        payload = jwt.decode(auth_token, current_app.config.get('SECRET_KEY'))
        return payload['sub']
    except jwt.ExpiredSignatureError:
        raise errors.ExpiredSignatureError()
    except jwt.InvalidTokenError:
        raise errors.InvalidTokenError()
        