from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


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
    model_config = SettingsConfigDict(env_nested_delimiter="__")

    db: DatabaseConnection
    oath2: OAuth2


settings = Settings()
