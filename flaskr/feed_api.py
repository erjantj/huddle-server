"""Feed api handlers."""
import flask

from flaskr import forms
from flaskr import schemas
from flaskr import auth_service as auth
from flaskr import feed_service

# pylint: disable=invalid-name
bp = flask.Blueprint('feed', __name__)


@bp.route('/subscribe', methods=['POST'])
@auth.login_required
@forms.form_handler(forms.SubscriptionForm)
def subscribe(data: dict):
    """Subscribe endpoint handler."""
    user = auth.get_user()
    feed_service.subscribe(user, data['source_id'])


@bp.route('/search', methods=['GET'])
@auth.login_required
@forms.form_handler(forms.SearchForm, schemas.SourceSchema(many=True))
def search(data: dict) -> list:
    """Search endpoint handler."""
    return feed_service.search(data['q'])


@bp.route('/', methods=['GET'])
@auth.login_required
@forms.form_handler(forms.FeedForm, schemas.PostSchema(many=True))
def feed(data: dict) -> list:
    """Feed endpoint handler."""
    page = data.get('page', 1)
    user = auth.get_user()
    return feed_service.feed(user, page)
