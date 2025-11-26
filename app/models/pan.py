"""
Modelo hijo: Pan
Hereda de Producto usando PostgreSQL INHERITS
"""
from sqlalchemy import Integer, Enum as SQLEnum, Column, Text, String
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base
from .producto import Producto
from .types import TypeBread
from typing import List


class Pan(Producto):
    """
    Tabla hija: pan (INHERITS producto)
    
    Atributos adicionales:
    - tipo_pan: ENUM type_bread
    - precio: Composite type price_amount (retail_sale, wholesale)
    - ingredientes: ARRAY de TEXT
    
    NOTA: precio es un tipo compuesto PostgreSQL (price_amount).
    SQLAlchemy no mapea automáticamente composite types, por lo que se
    maneja como columna genérica y se procesa en la capa de aplicación.
    
    NOTA 2: En PostgreSQL con INHERITS, la tabla hija contiene TODAS las columnas
    de la tabla padre, por lo que SQLAlchemy necesita declarar todas las columnas.
    """
    __tablename__ = "pan"
    
    # IMPORTANTE: En PostgreSQL INHERITS, la tabla hija tiene todas las columnas
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    
    # Columnas heredadas de Producto
    nombre: Mapped[str] = mapped_column(String(50), nullable=False)
    descripcion: Mapped[str | None] = mapped_column(Text, nullable=True)
    imagen_url: Mapped[str] = mapped_column(Text, nullable=False)
    
    # Columnas propias del pan
    tipo_pan: Mapped[TypeBread | None] = mapped_column(
        SQLEnum(TypeBread, name="type_bread", create_type=False, values_callable=lambda x: [e.value for e in x]),
        nullable=True
    )
    
    # Tipo compuesto price_amount: (retail_sale, wholesale)
    # Se mapea como Column porque SQLAlchemy no soporta bien COMPOSITE
    # PostgreSQL devuelve esto como tupla ROW type
    precio = Column("precio", nullable=True)
    
    # Disponibilidad del producto
    disponible = Column("disponible", nullable=True)
    
    # Array de ingredientes
    ingredientes: Mapped[List[str] | None] = mapped_column(
        ARRAY(Text),
        nullable=True
    )
    
    __mapper_args__ = {
        "polymorphic_identity": "pan",
        "concrete": True,
    }
    
    def __repr__(self) -> str:
        return f"<Pan(id={self.id}, nombre='{self.nombre}', tipo='{self.tipo_pan}')>"
