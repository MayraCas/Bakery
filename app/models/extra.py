"""
Modelo hijo: Extra
Hereda de Producto usando PostgreSQL INHERITS
"""
from sqlalchemy import Integer, Enum as SQLEnum, Column, Text, String
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base
from .producto import Producto
from .types import TypeExtra


class Extra(Producto):
    """
    Tabla hija: extra (INHERITS producto)
    
    Atributos adicionales:
    - tipo_extra: ENUM type_extra
    - precio: Composite type price_amount (retail_sale, wholesale)
    
    NOTA: precio es un tipo compuesto PostgreSQL (price_amount).
    SQLAlchemy no mapea automáticamente composite types, por lo que se
    maneja como columna genérica y se procesa en la capa de aplicación.
    
    NOTA 2: En PostgreSQL con INHERITS, la tabla hija contiene TODAS las columnas.
    """
    __tablename__ = "extra"
    
    # IMPORTANTE: En PostgreSQL INHERITS, la tabla hija tiene todas las columnas
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    
    # Columnas heredadas de Producto
    nombre: Mapped[str] = mapped_column(String(50), nullable=False)
    descripcion: Mapped[str | None] = mapped_column(Text, nullable=True)
    imagen_url: Mapped[str] = mapped_column(Text, nullable=False)
    
    # Columnas propias del extra
    tipo_extra: Mapped[TypeExtra | None] = mapped_column(
        SQLEnum(TypeExtra, name="type_extra", create_type=False, values_callable=lambda x: [e.value for e in x]),
        nullable=True
    )
    
    # Tipo compuesto price_amount: (retail_sale, wholesale)
    # Se mapea como Column porque SQLAlchemy no soporta bien COMPOSITE
    # PostgreSQL devuelve esto como tupla ROW type
    precio = Column("precio", nullable=True)
    
    __mapper_args__ = {
        "polymorphic_identity": "extra",
        "concrete": True,
    }
    
    def __repr__(self) -> str:
        return f"<Extra(id={self.id}, nombre='{self.nombre}', tipo='{self.tipo_extra}')>"
