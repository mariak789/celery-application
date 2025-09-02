import requests_mock
from sqlalchemy import select, func

from app.tasks.cards import fetch_credit_cards
from app.db.models import User, CreditCard


def test_fetch_cards_links_to_users(monkeypatch, db_session):
    # seed one user
    u = User(ext_id=1, name="A", username="a", email="a@a.a")
    db_session.add(u)
    db_session.commit()

    # make task use the test DB session
    monkeypatch.setattr("app.tasks.cards.SessionLocal", lambda: db_session)

    # 1) random-data-api returns a dict
    with requests_mock.Mocker() as m:
        m.get(
            "https://random-data-api.com/api/v2/credit_cards?size=1",
            json={"credit_card_number": "4111111111111111", "credit_card_type": "visa"},
            status_code=200,
        )
        n = fetch_credit_cards()
        assert n == 1

    # 2) random-data-api returns a list with one dict
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

    cnt = db_session.execute(select(func.count()).select_from(CreditCard)).scalar_one()
    assert cnt == 2