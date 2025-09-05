from __future__ import annotations

import logging
from typing import Any

from faker import Faker
from sqlalchemy import select

from app.celery_app import celery_app
from app.db.base import SessionLocal
from app.db.models import User
from app.db.repositories import create_card_for_user

log = logging.getLogger(__name__)

_fake = Faker()


def _generate_card(fake: Faker = _fake) -> dict[str, Any]:
    number = fake.credit_card_number()
    card_type = fake.credit_card_provider()
    return {"number": number, "type": card_type}


@celery_app.task(name="fetch_credit_cards")
def fetch_credit_cards() -> int:
    saved = 0
    with SessionLocal() as db:
        users = db.execute(select(User).order_by(User.id)).scalars().all()
        for u in users:
            item = _generate_card()
            create_card_for_user(
                db,
                user_id=u.id,
                number=str(item["number"]),
                type_=str(item["type"]),
            )
            saved += 1
    log.info("fetch_credit_cards: %s rows", saved)
    return saved
