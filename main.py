from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db
from src.router import client, channel, product
from src.schema import DomainSchema


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

app.include_router(client.clients_router)
app.include_router(channel.channel_router)
app.include_router(product.products_router)


@app.post("/op_facade/domMgmt/CreateDomain")
async def create_domain(domain_data: DomainSchema, session: AsyncSession = Depends(get_db)):
    try:

        new_domain = await orm.create_domain(session, domain_data.title, domain_data.descr)
        return {"message": f"Domain {new_domain.title} created successfully."}
    except IntegrityError as ex:
        await session.rollback()
        raise HTTPException(status_code=400, detail=f"IntegrityError: {str(ex)}")
    except Exception as ex:
        await session.rollback()
        raise HTTPException(status_code=500, detail=str(ex))


@app.get("/reload/")
async def reload_db():
    await orm.AsyncORM.create_tables()
    return
