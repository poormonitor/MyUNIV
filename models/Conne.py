"""
This file defines the connection model, which joins must and major.
"""
from . import db


class Conne(db.Model):
    __tablename__ = 'conne'
    connid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    mid = db.Column(db.Integer, nullable=False, index=True)
    mmid = db.Column(db.Integer, nullable=False, index=True)
    year = db.Column(db.Integer, nullable=False, index=True)

    def __repr__(self):
        return '<Conne %r>' % self.connid

    def __init__(self, mid, mmid, year):
        self.mid = mid
        self.mmid = mmid
        self.year = year
