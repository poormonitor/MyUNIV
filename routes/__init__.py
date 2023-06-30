import time

from fastapi import Depends, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from misc.auth import admin_required, get_current_user
from config import get_version


def init_app_routes(app: FastAPI):
    from .list import router as list_router
    from .get import router as get_router
    from .query import router as query_router
    from .user import router as user_router
    from .users import router as users_router
    from .manage import router as manage_router

    app.include_router(list_router, prefix="/api/list", tags=["list"])
    app.include_router(get_router, prefix="/api/get", tags=["get"])
    app.include_router(query_router, prefix="/api/query", tags=["query"])
    app.include_router(user_router, prefix="/api/user", tags=["user"])
    app.include_router(
        users_router,
        prefix="/api/users",
        tags=["users"],
        dependencies=[Depends(admin_required)],
    )
    app.include_router(
        manage_router,
        prefix="/api/manage",
        tags=["manage"],
        dependencies=[Depends(get_current_user)],
    )

    @app.get("/")
    def index():
        return FileResponse(path="views/dist/index.html")

    static_app = FastAPI()
    static_app.mount("/", StaticFiles(directory="views/dist"), name="index")

    @static_app.middleware("http")
    async def add_cache_control_static(request: Request, call_next):
        response = await call_next(request)
        response.headers["Cache-Control"] = "public, max-age=2592000"
        return response

    app.mount("/", static_app, name="static")

    @app.middleware("http")
    async def add_header(request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(round(process_time * 1000, 4))
        response.headers["X-MyUniv-Version"] = get_version()
        return response

    @app.middleware("http")
    async def add_cache_control(request: Request, call_next):
        response = await call_next(request)
        if "Cache-Control" not in response.headers:
            for tp in ["image", "font", "css", "javascript"]:
                if tp in response.headers.get("Content-Type", ""):
                    response.headers["Cache-Control"] = "public, max-age=2592000"
                    break
            else:
                response.headers["Cache-Control"] = "no-store"
        return response

    app.add_middleware(
        CORSMiddleware,
        allow_origins="*",
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
