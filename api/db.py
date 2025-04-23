from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from api.config import settings


engine = create_engine(
    settings.sqlalchemy_database_url,
    pool_pre_ping=True,
)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
