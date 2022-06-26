from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def init_app(app):
    from . import Conne, User, Major, Rank, Univ, Tag, Must

    db.init_app(app)
    return db
