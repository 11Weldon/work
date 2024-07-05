from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.queries.orm import AsyncORM
from src.router import channel, household


def create_fastapi_app():
    app = FastAPI(title="FastAPI")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        allow_headers=["*"],
    )
    return app


app = create_fastapi_app()

app.include_router(channel.channel_router)
app.include_router(household.household_router)


@app.get("/reload/")
async def reload_db():
    await AsyncORM.create_tables()
    return
