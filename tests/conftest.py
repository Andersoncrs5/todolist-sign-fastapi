from typing import Final
from sqlalchemy import Engine
from sqlalchemy.engine import create_engine
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool
from api.configs.db.database import Base, get_db
import pytest

from main import app

SQLALCHEMY_DATABASE_URL: Final[str] = "sqlite:///:memory:"

engine: Final[Engine] = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal: Final[sessionmaker[Session]] = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(name="db_session")
def db_session_fixture():

    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

    Base.metadata.drop_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()

    try:    
        yield db
    finally:
        db.close()

@pytest.fixture(name="client")
def client_fixture(db_session):
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as client:
        yield client
    app.dependency_overrides.clear()