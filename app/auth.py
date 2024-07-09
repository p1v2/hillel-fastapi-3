from datetime import timedelta, datetime

from jose import jwt
from sqlalchemy import select

from app.db import SessionLocal
from app.models import UserModel
from app.utils import get_password_hash, verify_password

SECRET_KEY = "a very secret key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


async def create_user(username: str, password: str):
    async with SessionLocal() as session:
        user = UserModel(username=username, hashed_password=get_password_hash(password))
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user


async def get_user(username: str) -> UserModel | None:
    async with SessionLocal() as session:
        return (await session.execute(select(UserModel).filter(UserModel.username == username))).first()[0]


async def authenticate_user(username: str, password: str) -> UserModel | None:
    user = await get_user(username)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt