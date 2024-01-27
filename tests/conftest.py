from typing import Generator

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.database import get_db
from app.models import Base
from database import override_get_db, create_test_db, testing_engine


@pytest.fixture(scope="session", autouse=True)
def test_db():
    create_test_db()


@pytest.fixture(scope="function", autouse=True)
def db_cleanup():
    Base.metadata.drop_all(bind=testing_engine)
    Base.metadata.create_all(bind=testing_engine)


@pytest.fixture(scope="session")
def client() -> Generator:
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c


@pytest.fixture
def user_data() -> dict:
    return {"email": "test@test.com", "password": "pass123"}
    