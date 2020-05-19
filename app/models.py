from datetime import datetime
from flask import url_for
from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from hashlib import md5

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    exercise = db.relationship('Exercise', backref='user', lazy='dynamic')
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    #token = db.Column(db.String(32), index=True, unique = True)
    #token_expiration = db.Column(db.DateTime)
    #admin = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    '''Token support methods for api

    def get_token(self, expires_in=3600):
        now = datetime.utcnow()
        if self.token and self.token_expiration > now + timedelta(seconds=60):
            return self.token
        self.token = base64.b64encode(os.urandom(24)).decode('utf-8')
        self.token_expiration = now+timedelta(seconds=expires_in)
        db.session.add(self)
        return self.token

    def revoke_token(self):
        self.token_expiration = datetime.utcnow() - timedelta(seconds=1)

    @staticmethod
    def check_token(token):
        user = User.query.filter_by(token=token).first()
        if user is None or user.token_expiration < datetime.utcnow():
            return None
        return user'''

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)

    # Adding in dictionary methods to convert to JSON
    def to_dict(self, include_email=False):
        data = {
            'id': self.id,
            'username': self.username,
            'about_me': self.about_me,
            'last_seen': self.last_seen.isoformat() + 'Z',
            'exercise_count': self.exercise.count(),
            '_links': {
                'self': url_for('get_user', id=self.id),
                #'exercise': url_for('api.get_exercise', id=self.id),
                'avatar': self.avatar(128)
            }
        }
        if include_email:
            data['email'] = self.email
        return data

    def from_dict(self, data, new_user=False):
        if 'username' in data:
            self.username=data['username']
        if 'email' in data:
            self.email=data['email']

class Exercise(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    style = db.Column(db.String(140))
    time = db.Column(db.String(140))
    #distance = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Exercise {}>'.format(self.style)

    # Adding in dictionary methods to convert to JSON
    def to_dict(self):
        data = {
            'id': self.id,
            'style': self.style,
            'time': self.time,
            'timestamp': self.timestamp.isoformat() + 'Z',
        }
        return data

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

