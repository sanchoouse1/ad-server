from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy import select
from sqlalchemy_db.db import get_async_session
from sqlalchemy_db.models import Ad, User
from sqlalchemy.ext.asyncio import AsyncSession
from src.schemas import AdOut, AdDetailOut, AdCreate, BaseResponse

router = APIRouter()

@router.get("/", summary="Просмотр списка объявлений")
async def get_list_ads(session: AsyncSession = Depends(get_async_session)) -> list[AdOut]:
    result = await session.execute(select(Ad))
    return result.scalars().all()


@router.get("/{ad_id}", summary="Обычный просмотр одного объявления")
async def get_ad_detail(
    ad_id: str,
    session: AsyncSession = Depends(get_async_session)
) -> AdOut:
    ad = await session.get(Ad, ad_id)
    if not ad:
        raise HTTPException(404, detail="Объявление не найдено")
    return ad


@router.get("/{ad_id}/detail", summary="Детальный просмотр одного объявления")
async def get_ad_detail(
    ad_id: str,
    session: AsyncSession = Depends(get_async_session)
) -> AdDetailOut:
    ad = await session.get(Ad, ad_id)

    if not ad:
        raise HTTPException(status_code=404, detail="Объявление не найдено")

    await session.refresh(ad, attribute_names=["owner", "comments"])
    return ad


@router.post("/", summary="Разместить объявление")
async def create_ad(
    request: Request,
    data: AdCreate,
    session: AsyncSession = Depends(get_async_session)
) -> str:
    owner_id = request.cookies.get('user_id')
    if not owner_id:
        raise HTTPException(status_code=403, detail="Вы не авторизованы, войдите в систему")

    user = await session.get(User, owner_id)
    if not user:
        raise HTTPException(status_code=403, detail="Пользователь не найден")

    ad = Ad(**data.model_dump(), owner_id=owner_id)
    session.add(ad)
    await session.commit()
    await session.refresh(ad)

    return ad.id


@router.delete("/{ad_id}", summary="Удаление объявления")
async def delete_ad(
    request: Request,
    ad_id: str,
    session: AsyncSession = Depends(get_async_session)
) -> BaseResponse:
    owner_id = request.cookies.get('user_id')
    if not owner_id:
        raise HTTPException(status_code=403, detail="Вы не авторизованы, войдите в систему")

    ad = await session.get(Ad, ad_id)

    if not ad:
        raise HTTPException(status_code=404, detail="Объявление не найдено")

    if ad.owner_id != owner_id:
        raise HTTPException(status_code=403, detail="Вы не можете удалить это объявление")

    await session.delete(ad)
    await session.commit()
    return {"status_code": 200, "detail": "Объявление успешно удалено"}