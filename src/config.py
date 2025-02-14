from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path


class Settings(BaseSettings):
    DB_NAME: str

    model_config = SettingsConfigDict(env_file=Path(__file__).parent.parent / ".env")


settings = Settings()
