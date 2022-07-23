from func import connectMust
from server import app

with app.app_context():
    connectMust()