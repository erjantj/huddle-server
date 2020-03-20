import flask
import functools
import wtforms
from flaskr import errors
from flaskr import schemas


class SearchForm(wtforms.Form):
    q = wtforms.StringField('Query', [wtforms.validators.DataRequired(), wtforms.validators.Length(max=2500)])


class FeedForm(wtforms.Form):
    page = wtforms.IntegerField('Page', [wtforms.validators.NumberRange(max=1000), wtforms.validators.Optional()])


class SubscriptionForm(wtforms.Form):
    source_id = wtforms.IntegerField('Source id', [wtforms.validators.DataRequired()])


def form_handler(form_class=None, response_schema=None):
    def decorator(func):
        @functools.wraps(func)
        def new_function(*args, **kwargs):
            result = None
            if form_class:
                data = flask.request.get_json(force=True, silent=True) or {}
                form = form_class(data=data)
                if not form.validate():
                    raise errors.ValidationError(payload=form.errors)
                result = func(data, *args, **kwargs)
            else:
                result = func(*args, **kwargs)

            if response_schema and result:
                return response_schema.jsonify(result)

            return flask.jsonify({})
        return new_function
    return decorator