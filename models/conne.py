from sqlalchemy import Column, Integer
from . import Base


class Conne(Base):
    __tablename__ = "conne"

    connid = Column(Integer, primary_key=True, autoincrement=True)
    mid = Column(Integer, nullable=False, index=True)
    mmid = Column(Integer, nullable=False, index=True)
