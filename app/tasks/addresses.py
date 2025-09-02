import logging
from typing import Any

import requests
from celery import shared_task
from sqlalchemy import select

from app.db.base import SessionLocal
from app.db.models import User
from app.db.repositories import create_address_for_user

log = logging.getLogger(__name__)

ADDR_URL = "https://random-data-api.com/api/v2/addresses"


def _pick(value: dict[str, Any], *keys: str) -> str:
    """Utility: pick first present key from API payload."""
    for k in keys:
        if k in value and value[k] is not None:
            return str(value[k])
    return ""


@shared_task(name="fetch_addresses")
def fetch_addresses() -> int:
    """
    For each stored user:
    - request a random address from random-data-api
    - insert it linked to the user
    Returns number of created Address rows.
    """
    saved = 0
    with SessionLocal() as db:
        users = db.execute(select(User).order_by(User.id)).scalars().all()
        for u in users:
            # Ask the API for one address. It returns a dict (size=1) or list (size>1).
            resp = requests.get(ADDR_URL, params={"size": 1}, timeout=15)
            resp.raise_for_status()
            payload = resp.json()
            item: dict[str, Any] = payload[0] if isinstance(payload, list) else payload

            street = _pick(item, "street_address", "street_name", "full_address")
            city = _pick(item, "city")
            country = _pick(item, "country")
            create_address_for_user(db, user_id=u.id, street=street, city=city, country=country)
            saved += 1

    log.info("fetch_addresses: stored %s address rows", saved)
    return saved