import uvicorn
from fastapi import FastAPI


def build_app() -> FastAPI:
    app = FastAPI()
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