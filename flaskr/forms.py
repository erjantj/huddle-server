import flask
import functools
import wtforms
from . import errors
from . import schemas

class SearchForm(wtforms.Form):
    q = wtforms.StringField('Query', [wtforms.validators.DataRequired(), wtforms.validators.Length(max=2500)])


def form_handler(form_class, response_schema=None):
    def decorator(func):
        @functools.wraps(func)
        def new_function(*args, **kwargs):
            data = flask.request.json
            form = form_class(data=data)
            if not form.validate():
                raise errors.ValidationError(payload=form.errors)
            result = func(data, *args, **kwargs)
            return response_schema.jsonify(result)
        return new_function
    return decorator