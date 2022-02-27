# -*- coding: utf-8 -*-
# @Time    : 2022/2/20 10:07
# @Author  : Johnson Sun (@poormonitor)
# @Email   : poormonitor@outlook.com
# @File    : app.py

from flask import Flask
from models import init_app as models_init_app
from routes import init_app as routes_init_app
from flask_migrate import Migrate
import os

migrate = Migrate()


def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = os.urandom(24)
    app.config['SESSION_COOKIE_PATH'] = '/univ'
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
        os.path.dirname(__file__), "data.db")
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

    db = models_init_app(app)
    migrate.init_app(app, db)
    routes_init_app(app)
    
    with app.app_context():
        db.create_all()
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(port=6000)
