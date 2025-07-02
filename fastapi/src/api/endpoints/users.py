from fastapi import APIRouter, Depends, HTTPException, Request, Response
from sqlalchemy import select
from sqlalchemy_db.db import get_async_session
from sqlalchemy_db.models import User, UserType
from sqlalchemy.ext.asyncio import AsyncSession
from src.schemas import UserFormData, BaseResponse

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

    # Разовая акция рождения первого админа
    if (new_user.email == "admin" and
        new_user.hashed_password == "admin"):
        new_user.role = UserType.ADMIN

    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)

    # TODO: Временное решение, убрать после JWT
    response.set_cookie(key="user_id", value=new_user.id)
    return new_user.id


@router.post("/login", summary="Вход в систему")
async def login_user(
    request: Request,
    response: Response,
    data: UserFormData,
    session: AsyncSession = Depends(get_async_session)
) -> str:
    # TODO: убрать после JWT
    user_id = request.cookies.get('user_id')
    if not user_id:
        raise HTTPException(status_code=403, detail="Вход запрещен. Проверьте корректность полей или зарегистрируйте новый аккаунт")
    
    result = await session.execute(select(User).where(User.id == data.user_id))
    existing_user = result.scalar_one_or_none()
    if existing_user:
        if (existing_user.hashed_password == data.hashed_password and
            existing_user.email == data.email):
            # TODO: Временное решение, убрать после JWT
            response.set_cookie(key="user_id", value=existing_user.id)
            return existing_user.id
        else:
            raise HTTPException(status_code=400, detail="Неверно введён логин или пароль")


@router.patch("/create-admin/{user_id}", summary="Назначить администратора")
async def create_admin(
    user_id: str,
    request: Request,
    session: AsyncSession = Depends(get_async_session)
) -> BaseResponse:
    current_admin_id = request.cookies.get('user_id')
    current_admin = await session.get(User, current_admin_id)
    if not current_admin or current_admin.role != UserType.ADMIN:
        raise HTTPException(status_code=403, detail="Недостаточно прав")
    
    user = await session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    
    user.role = UserType.ADMIN
    await session.commit()
    return {"status_code": 200, "detail": "Запрос выполнен успешно"}