# app/lifespan.py
from contextlib import asynccontextmanager
from fastapi import FastAPI
from database import Base, engine


@asynccontextmanager
async def lifespan(app:FastAPI):
    print('Starting')
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    print('Ending')
    await engine.dispose()