from celery import Celery
from app.core.config import settings

celery_app = Celery(
    "celery_application",
    broker=settings.redis_url,
    backend=settings.redis_url,
)

celery_app.conf.timezone = "UTC"
celery_app.autodiscover_tasks(["app.tasks"])

# Periodic tasks: tweak schedules as needed.
celery_app.conf.beat_schedule = {
    "fetch-users-every-5m": {
        "task": "fetch_users",
        "schedule": 300.0,
    },
    "fetch-addresses-every-10m": {
        "task": "fetch_addresses",
        "schedule": 600.0,
    },
    "fetch-cards-every-10m": {
        "task": "fetch_credit_cards",
        "schedule": 600.0,
    },
}