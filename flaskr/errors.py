"""Error classes."""


class BaseError(Exception):
    """Application errors base class."""
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
        """Converts error data to dictionary.

        Returns:
            Error dictionary.
        """
        error_dict = dict(self.payload or ())
        error_dict['message'] = self.message
        return error_dict


class InvalidUsernameOrPasswordError(BaseError):
    """Invalid username or password error."""
    status_code = 400
    message = 'Invalid username or password.'


class ExpiredSignatureError(BaseError):
    """Expired jwt signature error."""
    status_code = 401
    message = 'Signature expired. Please, log in again.'


class InvalidTokenError(BaseError):
    """Invalid jwt token error."""
    status_code = 401
    message = 'Invalid token. Please, log in again.'


class EncodingTokenError(BaseError):
    """Encoding jwt token error."""
    status_code = 400
    message = 'Unable to generate user authentication token.'


class UnauthorizedError(BaseError):
    """Unauthorized user error."""
    status_code = 401
    message = 'User is unauthorized. Please, log in.'


class ValidationError(BaseError):
    """Form data validation error."""
    status_code = 422
    message = 'Form contains validation errors.'


class SourceNotFoundError(BaseError):
    """Source not found error."""
    status_code = 404
    message = 'Source not found.'


class SourceParseError(BaseError):
    """Source parse error."""
    status_code = 400
    message = 'Unable to parse source.'


class UserNotFoundError(BaseError):
    """User not found error."""
    status_code = 404
    message = 'User not found.'
