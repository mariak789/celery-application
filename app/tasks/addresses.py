import logging
from typing import Any

import requests
from sqlalchemy import select

from app.celery_app import celery_app
from app.db.base import SessionLocal
from app.db.models import User
from app.db.repositories import create_address_for_user

log = logging.getLogger(__name__)
ADDR_URL = "https://fakerapi.it/api/v1/addresses?_locale=en_US&_quantity=1"


def _pick(d: dict[str, Any], *keys: str) -> str:
    for k in keys:
        v = d.get(k)
        if v is not None:
            return str(v)
    return ""


@celery_app.task(name="fetch_addresses")
def fetch_addresses() -> int:
    """For each user, fetch a random address and link it."""
    saved = 0
    with SessionLocal() as db:
        users = db.execute(select(User).order_by(User.id)).scalars().all()
        for u in users:
            r = requests.get(ADDR_URL, params={"size": 1}, timeout=15)
            r.raise_for_status()
            item = r.json()[0] if isinstance(r.json(), list) else r.json()
            create_address_for_user(
                db,
                user_id=u.id,
                street=_pick(item, "street_address", "street_name", "full_address"),
                city=_pick(item, "city"),
                country=_pick(item, "country"),
            )
            saved += 1
    log.info("fetch_addresses: %s rows", saved)
    return saved
