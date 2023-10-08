from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    PROJECT_NAME: str = "otus-4"
    API_V1_STR: str = "/api/v1"

    class Config:
        env_file = ".env"


settings = Settings()
