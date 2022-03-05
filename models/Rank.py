"""
This file defines the rank model, which contains rmid, mid, year, rank.
"""
from . import db


class Rank(db.Model):
    __tablename__ = 'rank'
    rmid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    mid = db.Column(db.Integer, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    rank = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<Rank %r>' % self.rmid

    def __init__(self, mid, year, rank):
        self.mid = mid
        self.year = year
        self.rank = rank