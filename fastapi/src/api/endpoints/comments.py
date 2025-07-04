from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy_db.db import get_async_session
from sqlalchemy_db.models import Ad, Comment, User, UserType
from src.schemas import CommentCreate, CommentOut, BaseResponse
from src.services.auth import get_current_user

router = APIRouter()


@router.post("/{ad_id}", summary="Добавить комментарий к объявлению")
async def add_comment(
    ad_id: str,
    data: CommentCreate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session)
) -> str:
    ad = await session.get(Ad, ad_id)
    if not ad:
        raise HTTPException(404, detail="Объявление не найдено")

    comment = Comment(text=data.text, ad_id=ad_id, author_id=current_user.id)
    session.add(comment)
    await session.commit()
    await session.refresh(comment)
    return comment.text


@router.delete("/{comment_id}", summary="Удалить комментарий")
async def delete_comment(
    comment_id: str,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session)
) -> BaseResponse:
    if current_user.role != UserType.ADMIN:
        raise HTTPException(403, detail="Недостаточно прав")

    comment = await session.get(Comment, comment_id)
    if not comment:
        raise HTTPException(404, detail="Комментарий не найден")

    await session.delete(comment)
    await session.commit()
    return {"status_code": 200, "detail": "Комментарий удалён"}
