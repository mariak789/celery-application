import logging
from typing import Any

import requests
from celery import shared_task
from sqlalchemy import select

from app.db.base import SessionLocal
from app.db.models import User
from app.db.repositories import create_card_for_user

log = logging.getLogger(__name__)

CARDS_URL = "https://random-data-api.com/api/v2/credit_cards"


def _as_dict(payload: Any) -> dict[str, Any]:
    """Normalize API response to a single dict."""
    return payload[0] if isinstance(payload, list) else payload


@shared_task(name="fetch_credit_cards")
def fetch_credit_cards() -> int:
    """
    For each stored user:
    - request a random credit card from random-data-api
    - insert it linked to the user
    Returns number of created CreditCard rows.
    """
    saved = 0
    with SessionLocal() as db:
        users = db.execute(select(User).order_by(User.id)).scalars().all()
        for u in users:
            resp = requests.get(CARDS_URL, params={"size": 1}, timeout=15)
            resp.raise_for_status()
            item = _as_dict(resp.json())

            number = str(item.get("credit_card_number", item.get("cc_number", "")))
            type_ = str(item.get("credit_card_type", item.get("cc_type", "")))
            create_card_for_user(db, user_id=u.id, number=number, type_=type_)
            saved += 1

    log.info("fetch_credit_cards: stored %s card rows", saved)
    return saved