from datetime import datetime

from pydantic import BaseModel, EmailStr


class PostIn(BaseModel):
    title: str
    content: str
    published: bool = True


class PostOut(PostIn):
    id: int
    created_at: datetime
    owner_id: int

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


class TokenData(BaseModel):
    user_id: int
