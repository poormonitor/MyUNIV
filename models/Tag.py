"""
This file defines the tag model, which contains tid and tname.
"""
from . import db

class Tag(db.Model):
    __tablename__ = 'tag'
    tid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tname = db.Column(db.String(64), nullable=False, index=True)

    def __repr__(self):
        return '<Tag %r>' % self.tid

    def __init__(self, tname):
        self.tname = tname