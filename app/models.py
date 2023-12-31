from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.sql.expression import text


class Base(DeclarativeBase):
    pass


class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    content: Mapped[str]
    published: Mapped[bool]
    created_at: Mapped[datetime] = mapped_column(
        server_default=text("(TIMEZONE('utc', CURRENT_TIMESTAMP))")
    )
    owner_id: Mapped[int] = mapped_column(
        ForeignKey(column="users.id", ondelete="CASCADE"), nullable=False
    )


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True)
    password_hash: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(
        server_default=text("(TIMEZONE('utc', CURRENT_TIMESTAMP))")
    )


class Vote(Base):
    __tablename__ = "votes"

    user_id: Mapped[int] = mapped_column(
        ForeignKey(column="users.id", ondelete="CASCADE"), primary_key=True
    )
    post_id: Mapped[int] = mapped_column(
        ForeignKey(column="posts.id", ondelete="CASCADE"), primary_key=True
    )
