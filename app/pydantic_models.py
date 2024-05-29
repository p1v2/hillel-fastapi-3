from datetime import datetime

from pydantic import BaseModel
from typing import Optional


class ProductPayload(BaseModel):
    name: str
    price: float
    grade: Optional[str] = None
    color: Optional[str] = None
    spec: Optional[str] = None
    supplier: Optional[str] = None
    created_at: datetime


class ProductUpdatePayload(BaseModel):
    name: str
    price: float
    grade: Optional[str] = None
    color: Optional[str] = None
    spec: Optional[str] = None
    supplier: Optional[str] = None
    updated_at: datetime


class Product(ProductPayload):
    id: int

    class Config:
        orm_mode = True
        from_attributes = True


class PaginatedProductResponse(BaseModel):
    results: list[Product]
    total: int
    offset: int
    limit: int
    username: str


class User(BaseModel):
    username: str
    hashed_password: str

    class Config:
        orm_mode = True
        from_attributes = True
