import os

basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'mysql://root:password@localhost/huddle'
SQLALCHEMY_TRACK_MODIFICATIONS = False