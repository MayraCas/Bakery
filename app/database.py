"""
Configuración de la base de datos PostgreSQL
Motor SQLAlchemy 2.0 con soporte para tipos compuestos y herencia
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator

# URL de conexión a PostgreSQL
URL_DATABASE = 'postgresql://postgres:root@localhost:5432/panaderia'

# Crear engine con configuración optimizada
engine = create_engine(
    URL_DATABASE,
    echo=False,  # Cambiar a True para debug SQL
    pool_pre_ping=True,  # Verificar conexiones antes de usar
)

# SessionLocal factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


def get_db() -> Generator[Session, None, None]:
    """
    Dependency para obtener sesión de base de datos.
    Uso en FastAPI con Depends(get_db)
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
