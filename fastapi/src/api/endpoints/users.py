from fastapi import APIRouter, Depends, HTTPException, Request, Response
from sqlalchemy import select
from sqlalchemy_db.db import get_async_session
from sqlalchemy_db.models import User, UserType
from sqlalchemy.ext.asyncio import AsyncSession
from src.schemas import UserFormData, BaseResponse
from fastapi.security import OAuth2PasswordRequestForm
from src.services.auth import get_current_user, create_access_token

router = APIRouter()


@router.post("/register", summary="Регистрация пользователя")
async def register_user(
    data: UserFormData,
    session: AsyncSession = Depends(get_async_session)
) -> dict:
    result = await session.execute(select(User).where(User.email == data.email))
    existing_user = result.scalar_one_or_none()
    if existing_user:
        raise HTTPException(status_code=400, detail="Данная почта уже используется")

    new_user = User(
        email=data.email,
        hashed_password=data.hashed_password
    )

    # Разовая акция рождения первого админа
    if (new_user.email == "admin" and
        new_user.hashed_password == "admin"):
        new_user.role = UserType.ADMIN

    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)

    access_token = create_access_token(data={"sub": new_user.id})

    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/login", summary="Вход в систему")
async def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_async_session)
) -> dict:
    result = await session.execute(select(User).where(User.email == form_data.username))
    existing_user = result.scalar_one_or_none()
    if not existing_user or existing_user.hashed_password != form_data.password:
        raise HTTPException(
            status_code=401,
            detail="Неверный логин или пароль",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": existing_user.id})
    return {"access_token": access_token, "token_type": "bearer"}


@router.patch("/create-admin/{user_id}", summary="Назначить администратора")
async def create_admin(
    user_id: str,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session)
) -> BaseResponse:
    if current_user.role != UserType.ADMIN:
        raise HTTPException(status_code=403, detail="Недостаточно прав")

    user = await session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    try:
        user.role = UserType.ADMIN
        await session.commit()
        return {"status_code": 200, "detail": "Пользователь назначен администратором"}
    except:
        raise HTTPException(status_code=500, detail="Ошибка при обновлении пользователя")