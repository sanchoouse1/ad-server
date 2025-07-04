from pydantic import BaseModel
from uuid import uuid4
from sqlalchemy_db.models import AdType, UserType

class BaseResponse(BaseModel):
    status_code: int
    detail: str

class CommentOut(BaseModel):
    id: str
    text: str
    author_id: str
    ad_id: str


class UserInfo(BaseModel):
    id: str
    email: str
    role: UserType

class UserFormData(BaseModel):
    email: str
    hashed_password: str


class AdCreate(BaseModel):
    title: str
    description: str
    type: AdType

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


class CommentCreate(BaseModel):
    text: str
