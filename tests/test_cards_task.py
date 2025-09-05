from faker import Faker
from sqlalchemy import select

from app.db.models import CreditCard, User
from app.tasks.cards import _generate_card, fetch_credit_cards


class _CM:
    """contextmanager для підміни SessionLocal у тасці."""

    def __init__(self, s):
        self.s = s

    def __enter__(self):
        return self.s

    def __exit__(self, exc_type, exc, tb):
        pass


def test_generate_card_is_deterministic_with_seed():
    fake = Faker()
    fake.seed_instance(1234)
    a = _generate_card(fake)
    fake.seed_instance(1234)
    b = _generate_card(fake)
    assert a == b
    assert "number" in a and "type" in a
    assert isinstance(a["number"], str)
    assert isinstance(a["type"], str)


def test_fetch_credit_cards_creates_one_card_per_user(db_session, monkeypatch):
    users = [
        User(name=f"u{i}", username=f"u{i}", email=f"u{i}@example.com", ext_id=i)
        for i in range(3)
    ]
    db_session.add_all(users)
    db_session.commit()

    fake = Faker()
    fake.seed_instance(42)
    monkeypatch.setattr("app.tasks.cards._fake", fake, raising=True)

    monkeypatch.setattr(
        "app.tasks.cards.SessionLocal", lambda: _CM(db_session), raising=True
    )

    saved = fetch_credit_cards()
    assert saved == 3

    cards = db_session.execute(select(CreditCard)).scalars().all()
    assert len(cards) == 3
    user_ids = {u.id for u in users}
    assert all(c.user_id in user_ids for c in cards)
    assert all(isinstance(c.number, str) and len(c.number) >= 12 for c in cards)
