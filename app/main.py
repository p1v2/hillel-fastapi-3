import asyncio
from datetime import timedelta

import uvicorn
from fastapi import FastAPI, Depends, Query, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app import models
from app.auth import SECRET_KEY, ALGORITHM, get_user, authenticate_user, ACCESS_TOKEN_EXPIRE_MINUTES, \
    create_access_token, create_user
from app.database import SessionLocal, engine
from app.models import ProductModel
from app.pydantic_models import Product, ProductPayload, PaginatedProductResponse, User

from jose import jwt, JWTError

app = FastAPI()
# models.Base.metadata.create_all(bind=engine)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = await get_user(username)
    if user is None:
        raise credentials_exception
    return user


@app.get("/")
def hello_world():
    return "Hello, world!"


async def get_db():
    async with SessionLocal() as session:
        yield session


async def get_product_total_count() -> int:
    async with SessionLocal() as session:
        count_query = select(func.count()).select_from(ProductModel)
        return (await session.execute(count_query)).scalar()


async def get_products(offset, limit) -> list[ProductModel]:
    async with SessionLocal() as session:
        result = await session.execute(select(ProductModel).offset(offset).limit(limit))

        return result.scalars().all()


@app.get("/products", response_model=PaginatedProductResponse)
async def read_products(
        current_user: User = Depends(get_current_user),
        offset=Query(0),
        limit=Query(10, le=50),
):
    products, total = await asyncio.gather(
        get_products(0, 10),
        get_product_total_count()
    )

    return PaginatedProductResponse(
        results=products,
        total=total,
        offset=0,
        limit=10
    )


@app.post("/products", response_model=Product)
async def create_product(product: ProductPayload, db: AsyncSession = Depends(get_db)):
    async with db as session:
        product = ProductModel(**product.dict())

        session.add(product)
        await session.commit()
        await session.refresh(product)

        return product


@app.patch("/products/{product_id}", response_model=Product)
async def update_product(
    product_id: int,
    product_data: ProductPayload,
    db: AsyncSession = Depends(get_db)
):
    async with db as session:
        product = await session.get(ProductModel, product_id)
        if product is None:
            raise HTTPException(status_code=404, detail="Product not found")
        
        for key, value in product_data.dict(exclude_unset=True).items():
            setattr(product, key, value)
        
        await session.commit()
        await session.refresh(product)
        return product
    


@app.delete("/products/{product_id}")
async def delete_product(
    product_id: int,
    db: AsyncSession = Depends(get_db)
):
    async with db as session:
        product = await session.get(ProductModel, product_id)
        if product is None:
            raise HTTPException(status_code=404, detail="Product not found")

        session.delete(product)
        await session.commit()

        return {"message": "Product deleted successfully"}





@app.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )

    accept_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=accept_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/register")
async def register(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await create_user(form_data.username, form_data.password)

    accept_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=accept_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8001)