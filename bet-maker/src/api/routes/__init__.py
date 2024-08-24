from fastapi import FastAPI

from api.routes import (
    event,
    bet,
)


def setup_routes(app: FastAPI) -> None:
    app.include_router(event.router)
    app.include_router(bet.router)
