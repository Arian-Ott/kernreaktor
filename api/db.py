from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
from api.config import settings
from tenacity import retry, stop_after_attempt, wait_fixed
from sqlalchemy.exc import OperationalError


@retry(stop=stop_after_attempt(10), wait=wait_fixed(2))
def get_engine():
    print(settings.sqlalchemy_database_url)
    engine = create_engine(settings.sqlalchemy_database_url, pool_pre_ping=True)

    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))
    return engine


engine = get_engine()



SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
