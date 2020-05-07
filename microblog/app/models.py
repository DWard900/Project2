from datetime import datetime
from app import db
# Chap 5 of Mega Tutorial
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login
# Chap 6
from hashlib import md5

#UserMixin from Chap 5
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    # Chap 6 of Mega Tutorial
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    # Chap 5
    def __repr__(self):
        return '<User {}>'.format(self.username)

    # Chapter 5 of Mega Tutorial
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # Chap 6 of Mega Tutorial
    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)

# Chap 5 of Mega Tutorial
@login.user_loader
def load_user(id):
    return User.query.get(int(id))
