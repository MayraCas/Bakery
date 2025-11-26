"""
Modelo base: Producto (tabla padre)
Usa herencia joined-table de SQLAlchemy para mapear INHERITS de PostgreSQL
"""
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base


class Producto(Base):
    """
    Tabla padre: producto
    
    Todas las tablas hijas (postre, pan, bebida, extra) heredan estos atributos.
    SQLAlchemy usa joined-table inheritance para mapear la herencia nativa de PostgreSQL.
    """
    __tablename__ = "producto"
    
    # Columnas
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nombre: Mapped[str | None] = mapped_column(String(50), nullable=False)
    descripcion: Mapped[str | None] = mapped_column(Text, nullable=True)
    imagen_url: Mapped[str | None] = mapped_column(Text, nullable=False)
    
    # Configuración de herencia
    __mapper_args__ = {
        "polymorphic_identity": "producto",
    }
    
    def __repr__(self) -> str:
        return f"<Producto(id={self.id}, nombre='{self.nombre}')>"
