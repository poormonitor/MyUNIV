"""
This file defines the major model, which contains mid, mname, mtags, sid, must, year, rank, schedule.
"""
from . import db


class Major(db.Model):
    __tablename__ = 'major'
    mid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    mname = db.Column(db.String(64), nullable=False, index=True)
    sid = db.Column(db.Integer, nullable=False, index=True)

    def __repr__(self):
        return '<Major %r>' % self.mid

    def __init__(self, mname, sid):
        self.mname = mname
        self.sid = sid