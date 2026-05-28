"""Core configuration module."""

from pathlib import Path
from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "PDF Summarizer"
    upload_dir: Path = Path("uploads")
    max_file_size_mb: int = 10

    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "llama3.2"

    mongodb_url: str = "mongodb://localhost:27017"
    mongodb_db_name: str = "pdf_extractext"

    openrouter_api_key: str = ""
    openrouter_api_url: str = "https://openrouter.ai/api/v1"
    openrouter_model: str = "openrouter/free"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache
def get_settings() -> Settings:
    return Settings()
