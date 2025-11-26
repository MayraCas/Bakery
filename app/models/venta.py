"""
Modelos: Venta y VentaDetalle
No usan herencia, son tablas independientes con relación 1:N
"""
from sqlalchemy import Column, Integer, String, Date, Numeric, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import date
from decimal import Decimal
from typing import List
from .base import Base


class Venta(Base):
    """
    Tabla: venta
    
    Representa la cabecera de una venta.
    El precio_total se calcula automáticamente mediante trigger en la BD.
    """
    __tablename__ = "venta"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    detalles: Mapped[str | None] = mapped_column(String(200), nullable=True)
    fecha: Mapped[date | None] = mapped_column(Date, server_default=func.current_date(), nullable=True)
    precio_total: Mapped[Decimal | None] = mapped_column(Numeric(10, 2), nullable=True)
    
    # Relación uno a muchos con VentaDetalle
    detalles_venta: Mapped[List["VentaDetalle"]] = relationship(
        "VentaDetalle",
        back_populates="venta",
        cascade="all, delete-orphan"
    )
    
    def __repr__(self) -> str:
        return f"<Venta(id={self.id}, fecha='{self.fecha}', total={self.precio_total})>"


class VentaDetalle(Base):
    """
    Tabla: venta_detalle
    
    Representa cada producto vendido en una venta.
    
    NOTA IMPORTANTE:
    - id_producto NO tiene FK explícita hacia producto debido a la herencia.
    - La integridad referencial se valida mediante trigger (trg_verificar_producto_fk).
    - El stock se actualiza automáticamente mediante trigger (trg_gestion_stock).
    - El precio_total de la venta se recalcula mediante trigger (trg_calcular_total_venta).
    """
    __tablename__ = "venta_detalle"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    id_venta: Mapped[int] = mapped_column(Integer, ForeignKey("venta.id", ondelete="CASCADE"))
    id_producto: Mapped[int | None] = mapped_column(Integer, nullable=True)  # NO FK explícita
    cantidad: Mapped[int | None] = mapped_column(Integer, nullable=True)
    precio: Mapped[Decimal | None] = mapped_column(Numeric(10, 2), nullable=True)
    
    # Relación muchos a uno con Venta
    venta: Mapped["Venta"] = relationship("Venta", back_populates="detalles_venta")
    
    def __repr__(self) -> str:
        return f"<VentaDetalle(id={self.id}, id_venta={self.id_venta}, id_producto={self.id_producto}, cantidad={self.cantidad})>"
