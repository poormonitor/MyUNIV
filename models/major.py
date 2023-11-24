from sqlalchemy import Column, Integer, String
from . import Base


class Major(Base):
    __tablename__ = "major"
    
    mid = Column(Integer, primary_key=True, autoincrement=True)
    mname = Column(String(128), nullable=False, index=True)
    sid = Column(Integer, nullable=False, index=True)
