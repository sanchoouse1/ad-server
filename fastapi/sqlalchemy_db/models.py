from sqlalchemy import String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy_db.db import Base
from uuid import UUID, uuid4
import enum

class UserType(str, enum.Enum):
    ADMIN = "admin"
    MODER = "moder"
    USER = "user"

class User(Base):
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False, index=True)
    hashed_password: Mapped[str]
    role: Mapped[UserType] = mapped_column(default=UserType.USER)

    ads: Mapped[list["Ad"]] = relationship(back_populates="owner")
    comments: Mapped[list["Comment"]] = relationship(back_populates="author")


class AdType(str, enum.Enum):
    SALE = "sale"
    PURCHASE = "purchase"
    SERVICE = "service"

class Ad(Base):
    __tablename__ = "ads"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    title: Mapped[str] = mapped_column(String, index=True)
    description: Mapped[str] = mapped_column(Text)
    type: Mapped[AdType] = mapped_column(default=AdType.SALE)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))

    owner: Mapped["User"] = relationship(back_populates="ads")
    comments: Mapped[list["Comment"]] = relationship(back_populates="ad")


class Comment(Base):
    __tablename__ = "comments"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    text: Mapped[str] = mapped_column(Text)
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    ad_id: Mapped[int] = mapped_column(ForeignKey("ads.id", ondelete="CASCADE"))

    author: Mapped["User"] = relationship(back_populates="comments")
    ad: Mapped["Ad"] = relationship(back_populates="comments")
