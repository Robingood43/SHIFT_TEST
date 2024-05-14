from fastapi import FastAPI

from SHIFT.app.api.router.user.main import router

__all__ = ["router", "init_routers"]


def init_routers(app: FastAPI):
    app.include_router(router)
