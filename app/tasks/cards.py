import logging
from typing import Any
import requests
from sqlalchemy import select

from app.celery_app import celery_app
from app.db.base import SessionLocal
from app.db.models import User
from app.db.repositories import create_card_for_user

log = logging.getLogger(__name__)
CARDS_URL = "https://random-data-api.com/api/v2/credit_cards?size=1"

def _as_dict(p: Any) -> dict[str, Any]:
    return p[0] if isinstance(p, list) else p

@celery_app.task(name="fetch_credit_cards")
def fetch_credit_cards() -> int:
    """For each user, fetch a random credit card and link it."""
    saved = 0
    with SessionLocal() as db:
        users = db.execute(select(User).order_by(User.id)).scalars().all()
        for u in users:
            r = requests.get(CARDS_URL, params={"size": 1}, timeout=15)
            r.raise_for_status()
            item = _as_dict(r.json())
            number = str(item.get("credit_card_number", item.get("cc_number", "")))
            type_ = str(item.get("credit_card_type", item.get("cc_type", "")))
            create_card_for_user(db, user_id=u.id, number=number, type_=type_)
            saved += 1
    log.info("fetch_credit_cards: %s rows", saved)
    return saved