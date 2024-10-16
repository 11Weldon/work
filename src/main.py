from uvicorn import run as run_app

from src.api.routes.utils import BASE_DIR
from src.core.app import app

if __name__ == "__main__":
    run_app(
        app,
        host="0.0.0.0",
        port=8181,
        log_config=str(BASE_DIR.parent / "public/log_conf.yml")
    )