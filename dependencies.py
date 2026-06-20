# app/dependencies
from database import AsyncSessionLocal


async def get_advertisement_session():
    async with AsyncSessionLocal() as session:
        yield session