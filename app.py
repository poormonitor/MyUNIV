# -*- coding: utf-8 -*-
# @Time    : 2022/2/20 10:07
# @Author  : Johnson Sun (@poormonitor)
# @Email   : poormonitor@outlook.com
# @File    : app.py

from flask import Flask
from models import init_app as models_init_app
from routes import init_app as routes_init_app
import os

app = Flask(__name__)

app.config['SECRET_KEY'] = os.urandom(24)
app.config['SESSION_COOKIE_PATH'] = '/'

# init models
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
    os.path.dirname(__file__), "data.db")
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = models_init_app(app)
if os.path.exists("data.db") == False or os.path.getsize("data.db") == 0:
    with app.app_context():
        db.create_all()

# init routes
routes_init_app(app)

if __name__ == '__main__':
    app.run(debug=True)