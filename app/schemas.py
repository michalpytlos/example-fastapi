from datetime import datetime

from pydantic import BaseModel, EmailStr


class BasePost(BaseModel):
    title: str
    content: str
    published: bool = True


class Post(BasePost):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class UserIn(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str
