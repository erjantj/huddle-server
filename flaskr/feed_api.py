import flask

from . import forms
from . import schemas
from . import errors
from . import feed_service


bp = flask.Blueprint('feed', __name__)

tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol', 
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web', 
        'done': False
    }
]

@bp.route('/subscribe', methods=['POST'])
def register():
    return flask.jsonify({'tasks': tasks})
    
@bp.route('/search', methods=['GET'])
@forms.form_handler(forms.SearchForm, schemas.SourceSchema(many=True))
def search(data: dict) -> list:
    return feed_service.search(data['q'])
    