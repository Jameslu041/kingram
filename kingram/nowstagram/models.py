"""
数据库的类(表)
"""
from nowstagram import db, login_manager
from datetime import datetime


class User(db.Model):
    id_ = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(32))
    salt = db.Column(db.String(32))
    head_url = db.Column(db.String(256))
    images = db.relationship('Image')

    def __init__(self, username, password, head_url, salt=""):
        self.username = username
        self.password = password
        self.salt = salt
        self.head_url = head_url

    def __repr__(self):
        return '<User {0} {1}>'.format(self.id_, self.username)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return True

    def get_id(self):
        return self.id_


class Image(db.Model):
    id_ = db.Column(db.Integer, primary_key=True, autoincrement=True)
    url = db.Column(db.String(1024))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id_'))
    created_date = db.Column(db.DateTime)
    comments = db.relationship('Comment')
    user = db.relationship('User')

    def __init__(self, url, user_id):
        self.url = url
        self.user_id = user_id
        self.created_date = datetime.now()

    def __repr__(self):
        return '<Image {0} {1}>'.format(self.id_, self.url)


class Comment(db.Model):
    id_ = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.String(1024))
    image_id = db.Column(db.Integer, db.ForeignKey('image.id_'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id_'))
    status = db.Column(db.Integer, default=0)
    user = db.relationship('User')

    def __init__(self, content, image_id, user_id):
        self.content = content
        self.image_id = image_id
        self.user_id = user_id
        self.status = 0

    def __repr__(self):
        return '<Comment {0} {1}>'.format(self.id_, self.content)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
