from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from settings import Settings

SQLALCHEMY_DATABASE_URL = Settings.DATABASE_CONNECTION

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_database_session():
    try:
        db = SessionLocal()
        return db
    finally:
        db.close()


db = get_database_session()
