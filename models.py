# app/models.py
from datetime import datetime

from sqlalchemy.orm import mapped_column, MappedColumn
from sqlalchemy import Integer, String, DateTime, func, Float

from database import Base


class Advertisement(Base):
    __tablename__ = 'advertisement'
    id : MappedColumn[int] = mapped_column(Integer, primary_key=True)
    header : MappedColumn[str] = mapped_column(String, unique=True)
    description : MappedColumn[str] = mapped_column(String)
    price : MappedColumn[float] = mapped_column(Float)
    author : MappedColumn[str] = mapped_column(String)
    created_at : MappedColumn[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    def to_dict(self):
        return {
            "id": self.id,
            "header": self.header,
            "description": self.description,
            "price": self.price,
            "author": self.author,
            "created_at": self.created_at.isoformat(),
        }