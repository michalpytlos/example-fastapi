from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime
from sqlalchemy.sql.expression import text


class Base(DeclarativeBase):
    pass


class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    content: Mapped[str]
    published: Mapped[bool]
    created_at: Mapped[datetime] = mapped_column(server_default=text("CURRENT_TIMESTAMP AT TIME ZONE 'UTC'"))
