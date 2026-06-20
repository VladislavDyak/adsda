# app/schemas.py
from datetime import datetime
from pydantic import BaseModel


class CreateAdvertisementRequest(BaseModel):
    header:str
    description:str|None = None
    price:float
    author:str
    created_at:datetime

class CreateAdvertisementResponse(BaseModel):
    id:int

class UpdateAdvertisementRequest(BaseModel):
    header:str|None = None
    description:str|None = None
    price:float|None = None
    author:str|None = None
    created_at:datetime|None = None

class UpdateAdvertisementResponse(BaseModel):
    id:int
    header:str
    description:str
    price:float
    author:str
    created_at:datetime

class GetAdvertisementResponse(BaseModel):
    header:str
    description:str
    price:float
    author:str
    created_at:datetime

class OkResponse(BaseModel):
    status:str = 'OK'


class SearchAdvertisementParams(BaseModel):
    id:int|None = None
    header:str|None = None
    description:str|None = None
    price:float|None = None
    author:str|None = None
    created_at:datetime|None = None

class SearchAdvertisementResponse(BaseModel):
    id: int
    header: str
    description: str
    price: float
    author: str
    created_at: datetime
