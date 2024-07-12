from uvicorn import run as run_app

from core.app import app
from core.settings import BASE_DIR

if __name__ == "__main__":
    run_app(
        app,
        host="0.0.0.0",
        port=4567,
    )
