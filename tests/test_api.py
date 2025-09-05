from app.db.models import Address, CreditCard, User


def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json().get("status") == "ok"


def test_users_list(client, db_session):
    db_session.add_all(
        [
            User(ext_id=1, name="A", username="a", email="a@a.a"),
            User(ext_id=2, name="B", username="b", email="b@b.b"),
        ]
    )
    db_session.commit()

    r = client.get("/users")
    assert r.status_code == 200
    data = r.json()
    assert len(data) == 2
    assert data[0]["ext_id"] == 1


def test_user_details(client, db_session):
    u = User(ext_id=10, name="Jane", username="jane", email="j@e.com")
    db_session.add(u)
    db_session.flush()  # get u.id

    db_session.add_all(
        [
            Address(user_id=u.id, street="S", city="C", country="X"),
            CreditCard(user_id=u.id, number="4111", type="visa"),
        ]
    )
    db_session.commit()

    r = client.get(f"/users/{u.id}")
    assert r.status_code == 200
    body = r.json()
    assert body["id"] == u.id
    assert body["addresses"] and body["cards"]
