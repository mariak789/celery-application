from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str = (
        "postgresql+psycopg://postgres:postgres@localhost:5432/celery_app"
    )
    redis_url: str = "redis://localhost:6379/0"
    api_title: str = "Celery Application"

    # beat intervals
    users_interval: int = 300
    addresses_interval: int = 600
    cards_interval: int = 600

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False)


settings = Settings()
