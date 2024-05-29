from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from app.db import Base


class ProductModel(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    price = Column(Float)
    grade = Column(String, default=None)
    color = Column(String, default=None)
    spec = Column(String, default=None)
    supplier = Column(String, default=None)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    def __init__(self, name: str, price: float, **kwargs):
        super().__init__(name=name, price=price, **kwargs)


class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
