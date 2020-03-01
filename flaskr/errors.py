class BaseError(Exception):
    status_code = 500
    message = 'Internal error'
    
    def __init__(self, message=None, status_code=None, payload=None):
        Exception.__init__(self)
        if message is not None:
            self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


class InvalidUsernameOrPasswordError(BaseError):
    status_code = 400
    message = 'Invalid username or password.'


class ExpiredSignatureError(BaseError):
    status_code = 401
    message = 'Signature expired. Please log in again.'

class InvalidTokenError(BaseError):
    status_code = 401
    message = 'Invalid token. Please log in again.'    

class ValidationError(BaseError):
    status_code = 433
    message = 'Form contains validation errors.'    