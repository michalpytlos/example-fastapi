from pydantic import BaseModel
from pydantic_settings import BaseSettings


class DatabaseConnection(BaseModel):
    username: str
    password: str
    host: str
    port: int
    database: str


class Settings(BaseSettings):
    db: DatabaseConnection

    class Config:
        env_nested_delimiter = "__"


settings = Settings()