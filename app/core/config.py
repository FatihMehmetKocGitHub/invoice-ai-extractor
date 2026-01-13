from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Literal


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )

    # App
    APP_NAME: str = "invoice-ai-extractor"

    # Redis / Celery
    REDIS_URL: str = "redis://redis:6379/0"
    CELERY_BROKER_URL: str = "redis://redis:6379/1"
    CELERY_RESULT_BACKEND: str = "redis://redis:6379/2"

    # LLM mode
    # "" | "local" | "api"
    LLM_MODE: Literal["", "local", "api"] = ""

    # Local LLM (Ollama)
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "llama3.1"

    # Remote / API LLM
    LLM_API_BASE_URL: str = ""
    LLM_API_KEY: str = ""
    LLM_API_MODEL: str = ""

    # Legacy / compatibility (istersen sonra silersin)
    LLM_PROVIDER: str = "local_ollama"


settings = Settings()
