from sqlalchemy import Column, Integer
from . import Base


class Rank(Base):
    __tablename__ = 'rank'

    rmid = Column(Integer, primary_key=True, autoincrement=True)
    mid = Column(Integer, nullable=False, index=True)
    year = Column(Integer, nullable=False, index=True)
    rank = Column(Integer, nullable=False, index=True)
    score = Column(Integer, nullable=False, index=True)
    schedule = Column(Integer, nullable=False)