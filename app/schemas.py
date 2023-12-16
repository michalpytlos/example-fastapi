from pydantic import BaseModel


class BasePost(BaseModel):
    title: str
    content: str
    published: bool = True


class Post(BasePost):
    id: int

    class Config:
        orm_mode = True
 