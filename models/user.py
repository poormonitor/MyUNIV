from sqlalchemy import Column, String, Boolean, DateTime, func
from . import Base


class User(Base):
    __tablename__ = "user"

    uid = Column(String(32), primary_key=True)
    name = Column(String(64), nullable=False)
    admin = Column(Boolean, nullable=False, default=False)
    passwd = Column(String(64), nullable=False)
    last_login = Column(DateTime, nullable=False, default=func.now())
