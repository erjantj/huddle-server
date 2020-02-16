import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

app.config.from_pyfile('config.py', silent=True)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

@app.route('/')
def hello():
    return 'Hello, World!'
    
# app.register_blueprint(auth.bp)

