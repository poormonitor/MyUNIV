"""
This file defines the rank model, which contains rmid, mid, year, rank.
"""
from . import db


class Rank(db.Model):
    __tablename__ = 'rank'
    rmid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    mid = db.Column(db.Integer, nullable=False, index=True)
    year = db.Column(db.Integer, nullable=False, index=True)
    rank = db.Column(db.Integer, nullable=False, index=True)
    score = db.Column(db.Integer, nullable=False, index=True)
    schedule = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<Rank %r>' % self.rmid

    def __init__(self, mid, year, rank, schedule, score):
        self.mid = mid
        self.year = year
        self.rank = rank
        self.schedule = schedule
        self.score = score