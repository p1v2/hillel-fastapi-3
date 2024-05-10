from pydantic import BaseModel


class ProductPayload(BaseModel):
    name: str
    price: float
    description: str
    quantity: int


class Product(ProductPayload):
    id: int

    class Config:
        # orm_mode = True
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
        # orm_mode = True
        from_attributes = True
