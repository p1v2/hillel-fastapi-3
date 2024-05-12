from datetime import datetime

from pydantic import BaseModel


class ProductPayload(BaseModel):
    name: str
    price: float
    description: str
    category: str
    supplier: str
    order_by: float
    created_at: datetime

class ProductUpdate(BaseModel):
    name: str
    price: float
    description: str
    category: str
    supplier: str
    order_by: float
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
