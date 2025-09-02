import requests_mock

from app.tasks.cards import fetch_credit_cards
from app.db.models import User


def test_fetch_cards_links_to_users(monkeypatch, db_session):
    # seed one user
    db_session.add(User(ext_id=1, name="A", username="a", email="a@a.a"))
    db_session.commit()

    monkeypatch.setattr("app.tasks.cards.SessionLocal", lambda: db_session)

    # random-data-api can return dict or [dict]; test both paths

    # 1) dict payload
    with requests_mock.Mocker() as m:
        m.get(
            "https://random-data-api.com/api/v2/credit_cards?size=1",
            json={"credit_card_number": "4111111111111111", "credit_card_type": "visa"},
            status_code=200,
        )
        n = fetch_credit_cards()
        assert n == 1

    # 2) list payload
    with requests_mock.Mocker() as m:
        m.get(
            "https://random-data-api.com/api/v2/credit_cards?size=1",
            json=[
                {
                    "credit_card_number": "5555555555554444",
                    "credit_card_type": "mastercard",
                }
            ],
            status_code=200,
        )
        n = fetch_credit_cards()
        assert n == 1

    rows = db_session.execute("SELECT COUNT(*) FROM credit_cards").scalar()
    assert rows == 2