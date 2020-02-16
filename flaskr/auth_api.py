import flask

from . import models
from . import errors
from . import jwt

bp = flask.Blueprint('auth', __name__)

@bp.route('/me', methods=['GET'])
def me():
    auth_header = flask.request.headers.get('Authorization')
    auth_token = ''
    if auth_header:
        auth_token = auth_header.split(" ")[1]
    
    if auth_token:
        resp = jwt.decode_auth_token(auth_token)
        user = models.User.query.filter_by(id=resp).first()
        responseObject = {
            'status': 'success',
            'data': {
                'user_id': user.id,
                'email': user.email,
            }
        }
        return flask.jsonify(responseObject)
    
    return flask.jsonify({})


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