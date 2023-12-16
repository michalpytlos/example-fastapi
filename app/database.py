from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import sessionmaker

from .config import settings

DATABASE_URL = URL.create(drivername="postgresql+psycopg", **settings.db.model_dump())

engine = create_engine(DATABASE_URL, echo=False)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()
