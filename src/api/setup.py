import uvicorn
from fastapi import FastAPI

from .router import router


def setup_routers(app: FastAPI) -> None:
    app.include_router(router, prefix="/api")


def build_app() -> FastAPI:
    app = FastAPI()

    setup_routers(app)

    return app

async def run_api(
    host: str = "localhost",
    port: int = 8000,
) -> None:
    app = build_app()

    uv_cfg = uvicorn.Config(
        app=app,
        host=host,
        port=port,
    )
    await uvicorn.Server(uv_cfg).serve()