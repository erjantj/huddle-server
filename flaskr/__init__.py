"""Application entrypoint"""
import flask
import flask_sqlalchemy
import flask_migrate
import flask_marshmallow

import celery

from flaskr import config

# pylint: disable=invalid-name
db = flask_sqlalchemy.SQLAlchemy()
ma = flask_marshmallow.Marshmallow()
client = celery.Celery(__name__, broker=config.CELERY_BROKER_URL)


def create_app():
    """Initialize application."""
    app = flask.Flask(__name__)

    app.config.from_pyfile('config.py', silent=True)
    db.init_app(app)
    ma.init_app(app)
    flask_migrate.Migrate(app, db)
    client.conf.update(app.config)

    with app.app_context():
        # pylint: disable=import-outside-toplevel
        from flaskr import error_handlers
        from flaskr import auth_api
        from flaskr import feed_api

        app.register_blueprint(error_handlers.bp)

        app.register_blueprint(auth_api.bp, url_prefix='/api/v1/auth')
        app.register_blueprint(feed_api.bp, url_prefix='/api/v1/feed')
        app.add_url_rule('/', endpoint='index')

        return app
