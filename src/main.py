from uvicorn import run as run_app

from src.core.app import app

if __name__ == "__main__":
    run_app(
        app,
        host="0.0.0.0",
        port=8080,
    )
