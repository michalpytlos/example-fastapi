from datetime import datetime, timedelta

from jose import jwt
from passlib.context import CryptContext

from .config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(
        minutes=settings.oath2.access_token_expire_minutes
    )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, key=settings.oath2.secret_key, algorithm=settings.oath2.algorithm
    )
    return encoded_jwt
