import logging, requests
from app.celery_app import celery_app
from app.db.base import SessionLocal
from app.db.repositories import upsert_user

log = logging.getLogger(__name__)
USERS_URL = "https://fakerapi.it/api/v1/users?_locale=en_US&_quantity=10"

@celery_app.task(name="fetch_users")
def fetch_users() -> int:
    r = requests.get(USERS_URL, timeout=15)
    r.raise_for_status()
    items = r.json().get("data", [])
    saved = 0
    with SessionLocal() as db:
        for it in items:
            upsert_user(
                db,
                ext_id=int(it.get("id")),
                name=f"{it.get('firstname','')} {it.get('lastname','')}".strip(),
                username=str(it.get("username","")),
                email=str(it.get("email","")),
            )
            saved += 1
    log.info("fetch_users: %s rows", saved)
    return saved