# -*- coding: utf-8 -*-
# @Time    : 2022/2/20 10:07
# @Author  : Johnson Sun (@poormonitor)
# @Email   : poormonitor@outlook.com
# @File    : app.py

from flask import Flask
from models import init_app as models_init_app
from routes import init_app as routes_init_app
from models.User import User
import os


def create_app():
    app = Flask(__name__)
    database = os.path.join(os.path.dirname(__file__), "data.sqlite")
    app.config["SECRET_KEY"] = os.getenv("MyUNIVSecretKey", default=os.urandom(24))
    app.config["SESSION_COOKIE_PATH"] = "/"
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 2592000
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + database
    app.config["SQLALCHEMY_COMMIT_ON_TEARDOWN"] = True
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db = models_init_app(app)
    routes_init_app(app)
    exists = os.path.isfile(database)
    with app.app_context():
        db.create_all()
        if not exists:
            db.session.add(
                User(
                    uid="admin",
                    name="admin",
                    password="21232f297a57a5a743894a0e4a801fc3",
                    admin=True,
                )
            )
    return app


if __name__ == "__main__":
    app = create_app()
    app.run()
