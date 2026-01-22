from fastapi import FastAPI
from contextlib import asynccontextmanager
from dotenv import load_dotenv

from db.engine import engine
from db.base import Base
from routers.chat import router as create_details_router
from routers.chat import router as chat_router


# load environment variables (.env)
load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    # shutdown
    await engine.dispose()


app = FastAPI(
    title="LLM API",
    lifespan=lifespan
)


@app.get("/")
async def read_root():
    return {"message": "welcome"}


# include routers
app.include_router(create_details_router)
app.include_router(chat_router)
