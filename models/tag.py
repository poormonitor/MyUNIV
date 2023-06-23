from sqlalchemy import Column, Integer, String
from . import Base


class Tag(Base):
    __tablename__ = "tag"

    tid = Column(Integer, primary_key=True, autoincrement=True)
    tname = Column(String(64), nullable=False, index=True)
