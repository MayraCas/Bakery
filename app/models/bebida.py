"""
Modelo hijo: Bebida
Hereda de Producto usando PostgreSQL INHERITS
"""
from sqlalchemy import Integer, Boolean, Enum as SQLEnum, Column, Text, String
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base
from .producto import Producto
from .types import TypeDrink
from typing import List


class Bebida(Producto):
    """
    Tabla hija: bebida (INHERITS producto)
    
    Atributos adicionales:
    - tipo_bebida: ENUM type_drink
    - precio: Composite type price_size (small, medium, big)
    - ingredientes: ARRAY de TEXT
    - es_fria: BOOLEAN
    
    NOTA: precio es un tipo compuesto PostgreSQL (price_size).
    SQLAlchemy no mapea automáticamente composite types, por lo que se
    maneja como columna genérica y se procesa en la capa de aplicación.
    
    NOTA 2: En PostgreSQL con INHERITS, la tabla hija contiene TODAS las columnas.
    """
    __tablename__ = "bebida"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    
    nombre: Mapped[str] = mapped_column(String(50), nullable=False)
    descripcion: Mapped[str | None] = mapped_column(Text, nullable=True)
    imagen_url: Mapped[str] = mapped_column(Text, nullable=False)
    
    tipo_bebida: Mapped[TypeDrink | None] = mapped_column(
        SQLEnum(TypeDrink, name="type_drink", create_type=False, values_callable=lambda x: [e.value for e in x]),
        nullable=True
    )
    
    precio = Column("precio", nullable=True)
    
    disponible = Column("disponible", nullable=True)
    
    ingredientes: Mapped[List[str] | None] = mapped_column(
        ARRAY(Text),
        nullable=True
    )
    
    es_fria: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    
    __mapper_args__ = {
        "polymorphic_identity": "bebida",
        "concrete": True,
    }
    
    def __repr__(self) -> str:
        return f"<Bebida(id={self.id}, nombre='{self.nombre}', tipo='{self.tipo_bebida}')>"
