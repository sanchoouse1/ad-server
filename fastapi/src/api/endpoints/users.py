from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy import select
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
    result = await session.execute(select(User).where(User.email == data.email))
    existing_user = result.scalar_one_or_none()
    if existing_user:
        raise HTTPException(status_code=400, detail="Данная почта уже используется")

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


@router.post("/login", summary="Вход в систему")
async def login_user(
    response: Response,
    data: UserFormData,
    session: AsyncSession = Depends(get_async_session)
):
    pass