import requests_mock
from sqlalchemy import select, func

from app.tasks.users import fetch_users
from app.db.models import User


def test_fetch_users_inserts_rows(monkeypatch, db_session):
    # make task use the test DB session
    monkeypatch.setattr("app.tasks.users.SessionLocal", lambda: db_session)

    payload = {
        "status": "OK",
        "total": 2,
        "data": [
            {
                "id": 1,
                "firstname": "Ann",
                "lastname": "Lee",
                "username": "ann",
                "email": "a@a.a",
            },
            {
                "id": 2,
                "firstname": "Bob",
                "lastname": "Fox",
                "username": "bob",
                "email": "b@b.b",
            },
        ],
    }

    with requests_mock.Mocker() as m:
        m.get(
            "https://fakerapi.it/api/v1/users?_locale=en_US&_quantity=10",
            json=payload,
            status_code=200,
        )
        inserted = fetch_users()
        assert inserted == 2

    # verify rows in DB
    cnt = db_session.execute(select(func.count()).select_from(User)).scalar_one()
    assert cnt == 2