"""
This file defines the must model, which contains mmid, mid, year, must.
"""
from . import db


class Must(db.Model):
    __tablename__ = 'must'
    mmid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    mname = db.Column(db.String(64), nullable=False, index=True)
    year = db.Column(db.Integer, nullable=False, index=True)
    sid = db.Column(db.Integer, nullable=False, index=True)
    must = db.Column(db.Integer, nullable=False, index=True)
    include = db.Column(db.String(128), nullable=False, index=True)

    def __repr__(self):
        return '<Must %r>' % self.mmid

    def __init__(self, mname, year, sid, must, include=""):
        self.mname = mname
        self.year = year
        self.sid = sid
        self.must = must
        self.include = include