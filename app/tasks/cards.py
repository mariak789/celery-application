import logging
from typing import Any

import requests
from faker import Faker
from sqlalchemy import select

from app.celery_app import celery_app
from app.core.config import settings
from app.db.base import SessionLocal
from app.db.models import User
from app.db.repositories import create_card_for_user

log = logging.getLogger(__name__)
faker = Faker()


def _as_dict(p: Any) -> dict[str, Any]:
    return p[0] if isinstance(p, list) else p


@celery_app.task(name="fetch_credit_cards")
def fetch_credit_cards() -> int:
    """Fetch credit cards for users either from remote API or fallback to Faker."""
    saved = 0

    with SessionLocal() as db:
        users = db.execute(select(User).order_by(User.id)).scalars().all()
        for u in users:
            try:
                if settings.cards_provider == "remote":
                    r = requests.get(
                        settings.cards_url,
                        params={"size": 1},
                        timeout=settings.cards_timeout,
                    )
                    r.raise_for_status()
                    item = _as_dict(r.json())
                    number = str(
                        item.get("credit_card_number", item.get("cc_number", ""))
                    )
                    type_ = str(item.get("credit_card_type", item.get("cc_type", "")))
                else:
                    # fallback to Faker
                    number = faker.credit_card_number()
                    type_ = faker.credit_card_provider()

                create_card_for_user(db, user_id=u.id, number=number, type_=type_)
                saved += 1
            except Exception as e:
                log.error("Failed to fetch credit card for user %s: %s", u.id, e)

    log.info("fetch_credit_cards: %s rows", saved)
    return saved
