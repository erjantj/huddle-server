import flask
import datetime

from flaskr import db


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    social_id = db.Column(db.String(64), nullable=False, unique=True)
    social_service = db.Column(db.String(64), nullable=False)
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64), nullable=False)
    username = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), nullable=True)

    def __repr__(self):
        return '<User {}>'.format(self.username)    


class Source(db.Model):
    __tablename__ = 'source'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    description = db.Column(db.Text())
    url = db.Column(db.String(64), nullable=False, unique=True)
    feed_link = db.Column(db.String(64), nullable=False, unique=True)
    icon = db.Column(db.String(64))
    language = db.Column(db.String(64))

    created_at = db.Column(db.DateTime, nullable=False,
        default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False,
        default=datetime.datetime.utcnow)

    def __repr__(self):
        return '<Source {}>'.format(self.name)  


class Post(db.Model):
    __tablename__ = 'post'

    id = db.Column(db.Integer, primary_key=True)
    source_id = db.Column(db.Integer, db.ForeignKey("source.id"), nullable=False,)
    title = db.Column(db.String(64), nullable=False)
    content = db.Column(db.Text())
    link = db.Column(db.String(2000), nullable=False, unique=True)
    author = db.Column(db.String(64), nullable=False)

    fetched_at = db.Column(db.DateTime, nullable=False,
        default=datetime.datetime.utcnow)
    published_at = db.Column(db.DateTime, nullable=False,
        default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False,
        default=datetime.datetime.utcnow)

    source = db.relationship("Source", backref="posts")

    def __repr__(self):
        return '<Post {}>'.format(self.title)    



class SourceSubscription(db.Model):
    __tablename__ = 'source_subscription'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    source_id = db.Column(db.Integer, nullable=False)

    created_at = db.Column(db.DateTime, nullable=False,
        default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False,
        default=datetime.datetime.utcnow)

    def __repr__(self):
        return '<Source subscription {}>'.format(self.id)    

