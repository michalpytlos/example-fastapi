from typing import Literal

from pydantic import BaseModel, Field
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


class LoggingSettings(BaseModel):
    level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"
    directory: str = "./logs"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_nested_delimiter="__")

    db: DatabaseConnection
    oath2: OAuth2
    log: LoggingSettings = Field(default_factory=LoggingSettings)


settings = Settings()
