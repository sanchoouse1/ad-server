from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy_db.db import get_async_session
from sqlalchemy_db.models import Ad
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
    data: AdCreate,
    session: AsyncSession = Depends(get_async_session)
    ) -> str:
    ad = Ad(**data.model_dump())
    session.add(ad)
    await session.commit()
    await session.refresh(ad)


@router.delete("/{ad_id}")
async def delete_ad(
    ad_id: str,
    session: AsyncSession = Depends(get_async_session)
) -> BaseResponse:
    ad = await session.get(Ad, ad_id)

    if not ad:
        raise HTTPException(status_code=404, detail="Объявление не найдено")
    
    await session.delete(ad)
    await session.commit()
    return {"status_code": 200, "detail": "Объявление успешно удалено"}