import logging
from typing import Any

import requests
from celery import shared_task

from app.db.base import SessionLocal
from app.db.repositories import upsert_user

log = logging.getLogger(__name__)

# Public test API with 10 demo users
USERS_URL = "https://jsonplaceholder.typicode.com/users"


@shared_task(name="fetch_users", autoretry_for=(requests.RequestException,), retry_backoff=5, retry_kwargs={"max_retries": 3})
def fetch_users() -> int:
    """
    Periodic Celery task:
    1) Fetch users from JSONPlaceholder.
    2) Upsert them into the DB by external id (idempotent).
    Returns number of processed users.
    """
    # 1) Pull data
    resp = requests.get(USERS_URL, timeout=15)
    resp.raise_for_status()
    payload: list[dict[str, Any]] = resp.json()

    # 2) Store
    saved = 0
    with SessionLocal() as db:
        for row in payload:
            upsert_user(
                db,
                ext_id=int(row["id"]),
                name=str(row.get("name", "")),
                username=str(row.get("username", "")),
                email=str(row.get("email", "")),
            )
            saved += 1

    log.info("fetch_users: stored %s users", saved)
    return saved