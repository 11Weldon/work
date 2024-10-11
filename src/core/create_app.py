from typing import Callable, AsyncGenerator, Any

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.api.routes import api_router


def create_app(
    lifespan: Callable[[FastAPI], AsyncGenerator[None, None]] | None = None
) -> FastAPI:
    params: dict[str, Any] = {
        "title": "Test",
        "version": "1.0.0",
        "redoc_url": None,
        # "docs_url": None,
        "separate_input_output_schemas": False,
    }
    if lifespan is not None:
        params.update(lifespan=lifespan)
    app = FastAPI(**params)
    app.include_router(api_router)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return app