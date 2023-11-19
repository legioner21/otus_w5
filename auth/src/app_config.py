from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    PROJECT_NAME: str = "otus-5-auth"
    API_V1_STR: str = "/api/v1"
    DATABASE_URL: str = Field(..., env="DATABASE_URL")
    JWT_SECRET_KEY: str = "e3829436-269f-4503-a58c-4aad6efdf7bf"
    ACCESS_TOKEN_EXPIRE: int = 60 * 15
    REFRESH_TOKEN_EXPIRE: int = 60 * 60 * 24 * 30

    class Config:
        env_file = ".env"


settings = Settings()
