import os

import flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()

def create_app():
    app = flask.Flask(__name__)

    app.config.from_pyfile('config.py', silent=True)
    db.init_app(app)
    migrate = Migrate(app, db)

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
    
