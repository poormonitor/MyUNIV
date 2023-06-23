from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config import get_config

DATABASE_URL: str = get_config("DB_PATH")

c_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
e_args = {"pool_recycle": 3600} if "mysql" in DATABASE_URL else {}

engine = create_engine(DATABASE_URL, connect_args=c_args, **e_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
