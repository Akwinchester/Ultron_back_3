import os
from typing import Literal
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    MODE: Literal["DEV", "TEST", "PROD", "DOCKER"]
    LOG_LEVEL: str

    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int

    @property
    def DATABASE_URL(self):
        return (f"postgresql+asyncpg://"
                f"{self.POSTGRES_USER}:"
                f"{self.POSTGRES_PASSWORD}@"
                f"{self.POSTGRES_HOST}:"
                f"{self.POSTGRES_PORT}/"
                f"{self.POSTGRES_DB}")

    TEST_POSTGRES_DB: str
    TEST_POSTGRES_USER: str
    TEST_POSTGRES_PASSWORD: str
    TEST_POSTGRES_HOST: str
    TEST_POSTGRES_PORT: int

    @property
    def TEST_DATABASE_URL(self):
        return (f"postgresql+asyncpg://"
                f"{self.TEST_POSTGRES_USER}:"
                f"{self.TEST_POSTGRES_PASSWORD}@"
                f"{self.TEST_POSTGRES_HOST}:"
                f"{self.TEST_POSTGRES_PORT}/"
                f"{self.TEST_POSTGRES_DB}")

    @property
    def SYNC_DATABASE_URL(self):
        return (f"postgresql://"
                f"{self.POSTGRES_USER}:"
                f"{self.POSTGRES_PASSWORD}@"
                f"{self.POSTGRES_HOST}:"
                f"{self.POSTGRES_PORT}/"
                f"{self.POSTGRES_DB}")

    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int

    model_config = SettingsConfigDict(env_file=".env", extra="allow")


settings: Settings = Settings()