"""
Modelo hijo: Postre
Hereda de Producto usando PostgreSQL INHERITS
"""
from sqlalchemy import Integer, Boolean, Enum as SQLEnum, Column, Text, String
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base
from .producto import Producto
from .types import TypeDessert
from typing import List


class Postre(Producto):
    """
    Tabla hija: postre (INHERITS producto)
    
    Atributos adicionales:
    - tipo_postre: ENUM type_dessert
    - precio: Composite type price_size (small, medium, big)
    - ingredientes: ARRAY de TEXT
    - es_dulce: BOOLEAN
    
    NOTA: precio es un tipo compuesto PostgreSQL (price_size).
    SQLAlchemy no mapea automáticamente composite types, por lo que se
    maneja como columna genérica y se procesa en la capa de aplicación.
    
    NOTA 2: En PostgreSQL con INHERITS, la tabla hija contiene TODAS las columnas
    de la tabla padre, por lo que SQLAlchemy necesita declarar todas las columnas
    como parte de __table__ pero hereda los tipos y comportamiento del padre.
    """
    __tablename__ = "postre"
    
    # IMPORTANTE: En PostgreSQL INHERITS, la tabla hija tiene todas las columnas
    # No hay foreign key, las columnas se replican
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    
    # Columnas heredadas de Producto (necesitan declararse para SQLAlchemy)
    nombre: Mapped[str] = mapped_column(String(50), nullable=False)
    descripcion: Mapped[str | None] = mapped_column(Text, nullable=True)
    imagen_url: Mapped[str] = mapped_column(Text, nullable=False)
    
    # Columnas propias del postre
    tipo_postre: Mapped[TypeDessert | None] = mapped_column(
        SQLEnum(TypeDessert, name="type_dessert", create_type=False, values_callable=lambda x: [e.value for e in x]),
        nullable=True
    )
    
    # Tipo compuesto price_size: (small, medium, big)
    # Se mapea como Column porque SQLAlchemy no soporta bien COMPOSITE
    # PostgreSQL devuelve esto como tupla ROW type
    precio = Column("precio", nullable=True)
    
    # Array de ingredientes
    ingredientes: Mapped[List[str] | None] = mapped_column(
        ARRAY(Text),
        nullable=True
    )
    
    es_dulce: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    
    __mapper_args__ = {
        "polymorphic_identity": "postre",
        "concrete": True,
    }
    
    def __repr__(self) -> str:
        return f"<Postre(id={self.id}, nombre='{self.nombre}', tipo='{self.tipo_postre}')>"
