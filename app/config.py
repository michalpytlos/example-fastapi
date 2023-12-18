from pydantic import BaseModel
from pydantic_settings import BaseSettings


class DatabaseConnection(BaseModel):
    username: str
    password: str
    host: str
    port: int
    database: str


class OAuth2(BaseModel):
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int


class Settings(BaseSettings):
    db: DatabaseConnection
    oath2: OAuth2

    class Config:
        env_nested_delimiter = "__"


settings = Settings()
