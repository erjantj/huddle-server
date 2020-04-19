"""Module contains applications configs and constants."""
import os

BASEDIR = os.path.abspath(os.path.dirname(__file__))

SECRET_KEY = os.getenv('SECRET_KEY', 'secret')

SQLALCHEMY_DATABASE_URI = '{engine}://{username}:{password}@{host}:{port}/{database}'.format(
    engine='mysql+pymysql',
    username='root',
    password='root',
    host='db',
    port=3306,
    database='huddle')

SQLALCHEMY_TRACK_MODIFICATIONS = False

CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'db+mysql://root:password@localhost/huddle'


OAUTH_CREDENTIALS = {
    'facebook': {
        'id': '828939950941433',
        'secret': '8a3ee19afe389bcbc5a54aefe1375971'
    },
    'twitter': {
        'id': '',
        'secret': ''
    }
}

JWT_TTL = 2 * 60 * 60  # 2 hours
