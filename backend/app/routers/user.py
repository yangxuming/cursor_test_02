from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..auth import hash_password, verify_password, create_access_token
from ..database import get_db
from ..models import User

router = APIRouter(prefix="/api", tags=["auth"])


class UserRegister(BaseModel):
    username: str = Field(min_length=2, max_length=50)
    password: str = Field(min_length=6)


class UserLogin(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    username: str


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register(data: UserRegister, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.username == data.username))
    if result.scalar_one_or_none():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username already exists")

    user = User(username=data.username, hashed_password=hash_password(data.password))
    db.add(user)
    await db.flush()

    token = create_access_token(user.id)
    return TokenResponse(access_token=token, username=user.username)


@router.post("/login", response_model=TokenResponse)
async def login(data: UserLogin, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.username == data.username))
    user = result.scalar_one_or_none()

    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")

    token = create_access_token(user.id)
    return TokenResponse(access_token=token, username=user.username)
