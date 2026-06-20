#app/app.py
from datetime import datetime
from typing import Annotated
from fastapi import FastAPI, Depends, HTTPException, status
import lifespan
from database import engine, Base, AsyncSessionLocal
import models, schemas
from schemas import CreateAdvertisementResponse
from sqlalchemy.ext.asyncio import AsyncSession
from dependencies import get_advertisement_session
from services import add_advertisement, get_advertisement, search_advertisement

app = FastAPI(
    title="purchase and sale service",
    description="This is a simple purchase and sale service",
    version="alpha 0.0.1",
    lifespan=lifespan.lifespan,
)

SessionDep = Annotated[AsyncSession, Depends(get_advertisement_session)]
SearchDep = Annotated[schemas.SearchAdvertisementParams, Depends(schemas.SearchAdvertisementParams)]


@app.post('/v1/advertisement', response_model=CreateAdvertisementResponse, summary="Create New Advertisement")
async def post_advertisement(request_data: schemas.CreateAdvertisementRequest, session: SessionDep):
    new_advertisement = await add_advertisement(session, models.Advertisement, request_data)
    return schemas.CreateAdvertisementResponse(id = new_advertisement.id)



@app.patch('/v1/advertisement/{advertisement_id}')
async def patch_advertisement(advertisement_id: int, update_data: schemas.UpdateAdvertisementRequest, session: SessionDep):
    patched_advertisement = await patch_advertisement(session, models.Advertisement,advertisement_id, update_data)
    return schemas.UpdateAdvertisementResponse(**patched_advertisement.to_dict())


@app.delete('/v1/advertisement/{advertisement_id}')
async def delete_advertisement(advertisement_id: int, session: SessionDep):
    await delete_advertisement(session, models.Advertisement, advertisement_id)


@app.get('/v1/advertisement/{advertisement_id}', response_model=schemas.GetAdvertisementResponse, summary="Get advertisement by ID")
async def get_advertisement_by_id(advertisement_id: int, session: SessionDep):
    advertisement = await get_advertisement(session, models.Advertisement, advertisement_id)
    return schemas.GetAdvertisementResponse(**advertisement.to_dict())


@app.get('/v1/advertisement', response_model = list[schemas.SearchAdvertisementResponse], summary="Search Advertisement")
async def get_advertisement_by_query(params:SearchDep, session: SessionDep):
    advertisements = await search_advertisement(session, models.Advertisement, params)
    return advertisements

