from json import load
from pathlib import Path
from typing import Any, AsyncGenerator

BASE_DIR = Path(__file__).parent.parent.parent


class MobileDatabaseLoader:
    def __init__(self, file: str):
        self.file = BASE_DIR.parent / file

    async def __call__(self) -> AsyncGenerator[Any, Any]:
        with open(self.file, "r", encoding="utf-8") as data:
            yield load(data)
