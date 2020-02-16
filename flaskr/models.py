from . import db

class User(UserMixin, db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    social_id = db.Column(db.String(64), nullable=False, unique=True)
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64), nullable=False)
    username = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), nullable=True)

    def __repr__(self):
        return '<User {}>'.format(self.username)    