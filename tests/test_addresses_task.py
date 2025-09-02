import requests_mock

from app.tasks.addresses import fetch_addresses
from app.db.models import User


def test_fetch_addresses_links_to_users(monkeypatch, db_session):
    # seed two users in the test DB
    db_session.add_all(
        [
            User(ext_id=1, name="A", username="a", email="a@a.a"),
            User(ext_id=2, name="B", username="b", email="b@b.b"),
        ]
    )
    db_session.commit()

    monkeypatch.setattr("app.tasks.addresses.SessionLocal", lambda: db_session)

    payload = {
        "status": "OK",
        "total": 2,
        "data": [
            {"street": "S1", "city": "C1", "country": "X"},
            {"street": "S2", "city": "C2", "country": "Y"},
        ],
    }

    with requests_mock.Mocker() as m:
        m.get(
            "https://fakerapi.it/api/v1/addresses?_locale=en_US&_quantity=10",
            json=payload,
            status_code=200,
        )
        saved = fetch_addresses()
        assert saved == 2

    # verify addresses written and linked
    count = db_session.execute("SELECT COUNT(*) FROM addresses").scalar()
    assert count == 2
    linked = db_session.execute(
        "SELECT COUNT(*) FROM addresses WHERE user_id IS NOT NULL"
    ).scalar()
    assert linked == 2