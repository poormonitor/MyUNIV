from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from . import Base


class User(Base):
    __tablename__ = "user"

    uid = Column(String(32), primary_key=True)
    name = Column(String(64), nullable=False)
    admin = Column(Boolean, nullable=False, default=False)
    passwd = Column(String(64), nullable=False)
    last_login = Column(DateTime, nullable=True)
    must = Column(Integer, nullable=True, default=0)
    mymajor = Column(Text, nullable=True, default=None)
