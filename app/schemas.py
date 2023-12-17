from pydantic import BaseModel
from datetime import datetime


class BasePost(BaseModel):
    title: str
    content: str
    published: bool = True


class Post(BasePost):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
 