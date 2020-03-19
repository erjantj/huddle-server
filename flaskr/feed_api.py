import flask

from . import forms
from . import schemas
from . import errors
from . import auth_service
from . import feed_service


bp = flask.Blueprint('feed', __name__)


@bp.route('/subscribe', methods=['POST'])
@forms.form_handler(forms.SubscriptionForm)
def subscribe(data: dict):
    user = auth_service.get_user()
    feed_service.subscribe(user, data['source_id'])


@bp.route('/search', methods=['GET'])
@forms.form_handler(forms.SearchForm, schemas.SourceSchema(many=True))
def search(data: dict) -> list:
    return feed_service.search(data['q'])
    

@bp.route('/', methods=['GET'])
@forms.form_handler(forms.FeedForm, schemas.PostSchema(many=True))
def feed(data: dict) -> list:
    page = data.get('page', 1)
    user = auth_service.get_user()
    return feed_service.feed(user, page)  
    