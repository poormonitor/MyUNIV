from sqlalchemy import Column, Integer, String, Text
from . import Base


class Must(Base):
    __tablename__ = "must"

    mmid = Column(Integer, primary_key=True, autoincrement=True)
    mname = Column(String(64), nullable=False, index=True)
    year = Column(Integer, nullable=False, index=True)
    sid = Column(Integer, nullable=False, index=True)
    must = Column(Integer, nullable=False, index=True)
    include = Column(Text, nullable=False, index=True)
