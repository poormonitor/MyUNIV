"""
This file defines the major model, which contains mid, mname, mtags, sid, must, year, rank, schedule.
"""
from . import db


class Major(db.Model):
    __tablename__ = 'major'
    mid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    mname = db.Column(db.String(64), nullable=False)
    mtags = db.Column(db.String(64), nullable=False)
    sid = db.ForeignKey('univ.sid')
    must = db.Column(db.Integer, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    rank = db.Column(db.Integer, nullable=True)
    schedule = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<Major %r>' % self.mid

    def __init__(self, mname, mtags, sid, must, year, rank, schedule):
        self.mname = mname
        self.mtags = mtags
        self.sid = sid
        self.must = must
        self.year = year
        self.rank = rank
        self.schedule = schedule