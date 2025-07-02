from pydantic import BaseModel
from uuid import uuid4
from sqlalchemy_db.models import AdType, UserType

class CommentOut(BaseModel):
    id: str
    text: str
    author_id: str
    ad_id: str


class UserInfo(BaseModel):
    id: str
    email: str
    role: UserType


class AdOut(BaseModel):
    id: str
    title: str
    description: str
    type: AdType
    owner_id: str

class AdDetailOut(BaseModel):
    id: str
    title: str
    description: str
    type: AdType
    owner: UserInfo
    comments: list[CommentOut]
