from sqlalchemy import Column, Integer, String, Float, DateTime, func

from Fast_Api.app.db import declarative_base

Base = declarative_base()

class ProductModel(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    price = Column(Float)
    description = Column(String, index=True)
    category = Column(String, index=True)
    supplier = Column(String, index=True)
    order_by = Column(Float, index=True)
    created_at = Column(DateTime(timezone=True), index=True, default=func.now())
    updated_at = Column(DateTime(timezone=True), index=True, default=func.now())

class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
