from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Database & Redis
    database_url: str = (
        "postgresql+psycopg://postgres:postgres@localhost:5432/celery_app"
    )
    redis_url: str = "redis://localhost:6379/0"
    api_title: str = "Celery Application"

    # Beat intervals
    users_interval: int = 300
    addresses_interval: int = 600
    cards_interval: int = 600

    # Credit cards provider
    cards_provider: str = "remote"  # "remote" or "faker"
    cards_url: str = "https://random-data-api.com/api/v2/credit_cards"
    cards_timeout: int = 10

    # Pydantic config
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False)


settings = Settings()
