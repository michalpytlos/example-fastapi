from typing import Generator

from psycopg.errors import DuplicateDatabase  # type: ignore
from sqlalchemy import create_engine, text
from sqlalchemy.engine.url import URL
from sqlalchemy.exc import ProgrammingError
from sqlalchemy.orm import sessionmaker

from app.config import settings
from app.database import DATABASE_URL

technical_engine = create_engine(DATABASE_URL, isolation_level="AUTOCOMMIT")


def get_test_db_url():
    test_db_dict = settings.db.model_dump()
    test_db_dict["database"] += "_test"
    return URL.create(drivername="postgresql+psycopg", **test_db_dict)


TEST_DATABASE_URL = get_test_db_url()

testing_engine = create_engine(TEST_DATABASE_URL, echo=False)
TestingSession = sessionmaker(autocommit=False, autoflush=False, bind=testing_engine)


def override_get_db() -> Generator:
    try:
        db = TestingSession()
        yield db
    finally:
        db.close()


def create_test_db():
    with technical_engine.connect() as conn:
        try:
            t = text(f"CREATE DATABASE {settings.db.database}_test")
            conn.execute(t)
        except ProgrammingError as e:
            if type(e.orig) is DuplicateDatabase:
                pass
            else:
                raise
