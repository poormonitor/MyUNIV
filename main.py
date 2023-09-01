from fastapi import FastAPI

from models import Base, engine
from routes import init_app_routes
from misc.func import create_admin


app = FastAPI(title="MyUNIV", version="0.1.0")

init_app_routes(app)

Base.metadata.create_all(bind=engine)
create_admin()
