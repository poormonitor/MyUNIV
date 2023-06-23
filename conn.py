from misc.func import connectMust
from main import app

with app.app_context():
    connectMust()