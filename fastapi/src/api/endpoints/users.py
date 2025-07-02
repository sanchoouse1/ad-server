from fastapi import APIRouter, Depends, Response
from sqlalchemy_db.db import get_async_session
from sqlalchemy_db.models import User
from sqlalchemy.ext.asyncio import AsyncSession
from src.schemas import UserFormData

router = APIRouter()


@router.post("/register", summary="Регистрация пользователя")
async def register_user(
    response: Response,
    data: UserFormData,
    session: AsyncSession = Depends(get_async_session)
) -> str:
    new_user = User(
        email=data.email,
        hashed_password=data.hashed_password
    )
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)

    # TODO: Временное решение, убрать после JWT
    response.set_cookie(key="user_id", value=new_user.id)
    return new_user.id


@router.post("/login")
async def login_user():
    pass