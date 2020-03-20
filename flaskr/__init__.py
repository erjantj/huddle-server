import os

import flask
import flask_sqlalchemy
import flask_migrate
import flask_marshmallow
from flaskr import config

import celery


db = flask_sqlalchemy.SQLAlchemy()
ma = flask_marshmallow.Marshmallow()
client = celery.Celery(__name__, broker=config.CELERY_BROKER_URL)

def create_app():
    app = flask.Flask(__name__)

    app.config.from_pyfile('config.py', silent=True)
    db.init_app(app)
    ma.init_app(app)
    migrate = flask_migrate.Migrate(app, db)
    client.conf.update(app.config)

    with app.app_context():
        from . import error_handlers
        from . import auth_api
        from . import feed_api

        app.register_blueprint(error_handlers.bp)
        
        app.register_blueprint(auth_api.bp, url_prefix='/api/v1/auth')
        app.register_blueprint(feed_api.bp, url_prefix='/api/v1/feed')
        app.add_url_rule('/', endpoint='index')

        return app

# @app.route('/')
# def index():
#     return flask.render_template('index.html')
    
