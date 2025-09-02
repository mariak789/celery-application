import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.db.base import Base, get_session


@pytest.fixture(scope="session")
def engine():
    """Create a dedicated in-memory SQLite engine for tests."""
    eng = create_engine("sqlite+pysqlite:///:memory:", future=True)
    # create all tables once for the whole test session
    Base.metadata.create_all(eng)
    yield eng
    Base.metadata.drop_all(eng)


@pytest.fixture()
def db_session(engine):
    """Provide a transaction-scoped Session for each test."""
    TestingSession = sessionmaker(
        bind=engine, autoflush=False, autocommit=False, future=True
    )
    with TestingSession() as s:
        yield s


@pytest.fixture()
def client(db_session):
    """
    FastAPI TestClient that uses the test DB session via dependency override.
    """

    def _get_session_override():
        yield db_session

    app.dependency_overrides[get_session] = _get_session_override
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()