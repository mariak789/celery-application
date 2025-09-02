import logging
from typing import Any
import requests

from app.celery_app import celery_app         
from app.db.base import SessionLocal
from app.db.repositories import upsert_user

log = logging.getLogger(__name__)
USERS_URL = "https://fakerapi.it/api/v1/users?_locale=en_US&_quantity=10"


@celery_app.task(                                 
    name="fetch_users",
    autoretry_for=(requests.RequestException,),
    retry_backoff=5,
    retry_kwargs={"max_retries": 3},
)
def fetch_users() -> int:
    """Fetch users from JSONPlaceholder and upsert into DB."""
    resp = requests.get(USERS_URL, timeout=15)
    resp.raise_for_status()
    payload: list[dict[str, Any]] = resp.json()

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