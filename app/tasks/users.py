from celery import shared_task

@shared_task
def fetch_users_task() -> str:
    return "ok"