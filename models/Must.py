"""
This file defines the must model, which contains mmid, mid, year, must.
"""
from . import db


class Must(db.Model):
    __tablename__ = 'must'
    mmid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    mid = db.Column(db.Integer, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    must = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<Must %r>' % self.mmid

    def __init__(self, mid, year, must):
        self.mid = mid
        self.year = year
        self.must = must