import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db.base import get_session
from app.db.models import Base
from app.main import app as fastapi_app


@pytest.fixture(scope="session")
def engine():
    """Single in-memory SQLite engine shared across threads."""
    eng = create_engine(
        "sqlite+pysqlite:///:memory:",
        future=True,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    Base.metadata.create_all(eng)
    return eng


@pytest.fixture()
def db_session(engine):
    """Clean schema per test and provide a fresh Session."""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    TestingSession = sessionmaker(
        bind=engine, autoflush=False, autocommit=False, future=True
    )
    with TestingSession() as s:
        yield s


@pytest.fixture()
def client(db_session):
    def _get_session_override():
        yield db_session

    fastapi_app.dependency_overrides[get_session] = _get_session_override
    with TestClient(fastapi_app) as c:
        yield c
    fastapi_app.dependency_overrides.clear()
