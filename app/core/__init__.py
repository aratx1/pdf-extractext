"""Core configuration module."""

from pathlib import Path
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "PDF Summarizer"
    upload_dir: Path = Path("uploads")
    max_file_size_mb: int = 10
    nvidia_api_key: str = ""
    nvidia_api_url: str = "https://integrate.api.nvidia.com/v1"
    ai_model: str = "meta/llama-3.2-90b-vision-instruct"
    mongo_uri: str = "mongodb://localhost:27017"
    mongo_db: str = "appdb"


@lru_cache
def get_settings() -> Settings:
    return Settings()
