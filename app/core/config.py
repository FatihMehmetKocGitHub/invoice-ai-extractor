from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    APP_NAME: str = "invoice-ai-extractor"
    REDIS_URL: str = "redis://redis:6379/0"   # docker-compose için
    CELERY_BROKER_URL: str = "redis://redis:6379/1"
    CELERY_RESULT_BACKEND: str = "redis://redis:6379/2"

    # LLM seçimi (placeholder)
    LLM_PROVIDER: str = "local_ollama"  # or "api"
    OLLAMA_BASE_URL: str = "http://localhost:11434"

settings = Settings()
