from fastapi import FastAPI
from contextlib import asynccontextmanager

from db.engine import engine
from db.base import Base
from routers.create_my_details_router import router as create_details_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def read_root():
    return {"message": "welcome"}


app.include_router(create_details_router)
