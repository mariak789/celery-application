from celery import Celery
from app.core.config import settings

celery_app = Celery(
    "celery_application",
    broker=settings.redis_url,
    backend=settings.redis_url,
    include=[
        "app.tasks.users",
        "app.tasks.addresses",
        "app.tasks.cards",
    ],
)

celery_app.conf.timezone = "UTC"
celery_app.autodiscover_tasks(["app.tasks"])

# Periodic tasks (intervals from .env)
celery_app.conf.beat_schedule = {
    "fetch-users-periodic": {
        "task": "fetch_users",
        "schedule": float(settings.users_interval),
    },
    "fetch-addresses-periodic": {
        "task": "fetch_addresses",
        "schedule": float(settings.addresses_interval),
    },
    "fetch-credit-cards-periodic": {
        "task": "fetch_credit_cards",
        "schedule": float(settings.cards_interval),
    },
}