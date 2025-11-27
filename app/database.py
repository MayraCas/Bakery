
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator

# URL de conexión a PostgreSQL
URL_DATABASE = 'postgresql://postgres:root@localhost:5432/panaderia'

engine = create_engine(
    URL_DATABASE,
    echo=False,  
    pool_pre_ping=True,  
)


SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
