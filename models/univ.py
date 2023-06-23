from sqlalchemy import Column, Integer, String
from . import Base


class Univ(Base):
    __tablename__ = "univ"

    sid = Column(Integer, primary_key=True, autoincrement=True)
    uname = Column(String(64), nullable=False, index=True)
    utags = Column(String(64), nullable=False)
    province = Column(Integer, nullable=False, index=True)
