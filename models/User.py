"""
This file defines the user model, which contains userid, name, email, password, and other information.
"""
from . import db


class User(db.Model):
    __tablename__ = 'user'
    uid = db.Column(db.String(32), primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)
    passwd = db.Column(db.String(64), nullable=False)
    last_login = db.Column(db.DateTime, nullable=True)
    must = db.Column(db.Integer, nullable=True)
    mymajor = db.Column(db.Text, nullable=True, default=None)

    def __repr__(self):
        return '<User %r>' % self.uid

    def __init__(self, uid, name, password, admin=False, must=0):
        self.uid = uid
        self.name = name
        self.passwd = password
        self.admin = admin
        self.must = must