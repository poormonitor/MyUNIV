"""
This file defines the univ model, which contains sid, uname, utags, province and other information.
"""
from . import db


class Univ(db.Model):
    __tablename__ = 'univ'
    sid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uname = db.Column(db.String(64), nullable=False, index=True)
    utags = db.Column(db.String(64), nullable=False)
    province = db.Column(db.Integer, nullable=False, index=True)

    def __repr__(self):
        return '<Univ %r>' % self.sid

    def __init__(self, uname, utags="", province=0):
        self.uname = uname
        self.utags = utags
        self.province = province