from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    database_url: str = "postgresql+psycopg://postgres:postgres@localhost:5432/celery_app"
    redis_url: str = "redis://localhost:6379/0"
    api_title: str = "Celery Application"

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False)

settings = Settings()