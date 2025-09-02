import re
import requests_mock
from sqlalchemy import select, func

from app.tasks.addresses import fetch_addresses
from app.db.models import User, Address


def test_fetch_addresses_links_to_users(monkeypatch, db_session):
    # seed users that addresses will be linked to
    db_session.add_all(
        [
            User(ext_id=1, name="A", username="a", email="a@a.a"),
            User(ext_id=2, name="B", username="b", email="b@b.b"),
        ]
    )
    db_session.commit()

    # make task use the test DB session
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
        # regex to match any query params on the endpoint
        m.get(
            re.compile(r"https://fakerapi\.it/api/v1/addresses.*"),
            json=payload,
            status_code=200,
        )
        saved = fetch_addresses()
        assert saved == 2

    # verify addresses written & linked
    cnt = db_session.execute(select(func.count()).select_from(Address)).scalar_one()
    assert cnt == 2
    linked_cnt = db_session.execute(
        select(func.count()).select_from(Address).where(Address.user_id.is_not(None))
    ).scalar_one()
    assert linked_cnt == 2