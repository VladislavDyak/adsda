# app/services.py
from datetime import datetime, timezone

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from asyncpg.exceptions import UniqueViolationError
import models
import schemas
from sqlalchemy import select


async def add_advertisement(
        session: AsyncSession,
        orm_model: type[models.Advertisement],
        item_data: schemas.CreateAdvertisementRequest
)->models.Advertisement:
    new_advertisement = orm_model(**item_data.model_dump())
    session.add(new_advertisement)
    try:
        await session.commit()
        await session.refresh(new_advertisement)
        return new_advertisement
    except IntegrityError as e:
        await session.rollback()
        if isinstance(e.orig, UniqueViolationError) and e.orig.pgcode == "23505":
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Item already exists")
        else:
            raise e


async def get_advertisement(
        session: AsyncSession,
        orm_model: type[models.Advertisement],
        item_id: int
)->models.Advertisement:
    stmt = select(orm_model).where(orm_model.id == item_id)
    result = await session.execute(stmt)
    advertisement = result.scalar_one_or_none()
    if not advertisement:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{orm_model.__name__} with id{id} not found")
    return advertisement


async def update_advertisement(
        session: AsyncSession,
        orm_model: type[models.Advertisement],
        item_id: int,
        advertisement_data: schemas.UpdateAdvertisementRequest
)->models.Advertisement:
    advertisement = await get_advertisement(session, orm_model, item_id)
    update_dict = advertisement_data.model_dump(exclude_unset=True)

    for key, value in update_dict.items():
        setattr(advertisement, key, value)

    await session.commit()
    await session.refresh(advertisement)
    return advertisement

async def delete_advertisement(session: AsyncSession, orm_model: type[models.Advertisement], item_id: int)->None:
    advertisement = await get_advertisement(session, orm_model, item_id)
    await session.delete(advertisement)
    await session.commit()

async def search_advertisement(session: AsyncSession, orm_model: type[models.Advertisement], params: schemas.SearchAdvertisementParams)->list:
    data = select(orm_model)
    if params.id is not None:
        data = data.where(orm_model.id == params.id)
    if params.header is not None:
        data = data.where(orm_model.header == params.header)
    if params.description is not None:
        data = data.where(orm_model.description == params.description)
    if params.price is not None:
        data = data.where(orm_model.price == params.price)
    if params.author is not None:
        data = data.where(orm_model.author == params.author)
    if params.created_at is not None:
        data = data.where(orm_model.created_at == params.created_at)

    result = await session.execute(data)
    return list(result.scalars().all())