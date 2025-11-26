"""
Schemas Pydantic para Venta y VentaDetalle
"""
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import date
from decimal import Decimal


# ============================================
# VENTA DETALLE SCHEMAS
# ============================================

class VentaDetalleBase(BaseModel):
    """Schema base para VentaDetalle - atributos comunes"""
    id_producto: Optional[int] = Field(None, description="ID del producto vendido")
    cantidad: Optional[int] = Field(None, ge=1, description="Cantidad vendida")
    precio: Optional[Decimal] = Field(None, ge=0, decimal_places=2, description="Precio unitario")


class VentaDetalleCreate(VentaDetalleBase):
    """
    Schema para crear un VentaDetalle
    
    NOTA: No se incluye id_venta porque se asigna automáticamente
    al crear la venta.
    """
    id_producto: int = Field(..., description="ID del producto vendido")
    cantidad: int = Field(..., ge=1, description="Cantidad vendida")
    precio: Decimal = Field(..., ge=0, decimal_places=2, description="Precio unitario")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id_producto": 1,
                "cantidad": 2,
                "precio": "380.00"
            }
        }
    )


class VentaDetalleUpdate(BaseModel):
    """Schema para actualizar un VentaDetalle - todos los campos opcionales"""
    id_producto: Optional[int] = Field(None, description="ID del producto vendido")
    cantidad: Optional[int] = Field(None, ge=1)
    precio: Optional[Decimal] = Field(None, ge=0, decimal_places=2)


class VentaDetalleOut(VentaDetalleBase):
    """Schema para retornar un VentaDetalle"""
    id: int = Field(..., description="ID del detalle")
    id_venta: int = Field(..., description="ID de la venta")
    
    model_config = ConfigDict(from_attributes=True)


# ============================================
# VENTA SCHEMAS
# ============================================

class VentaBase(BaseModel):
    """Schema base para Venta - atributos comunes"""
    detalles: Optional[str] = Field(None, max_length=200, description="Descripción de la venta")
    fecha: Optional[date] = Field(None, description="Fecha de la venta")
    precio_total: Optional[Decimal] = Field(None, ge=0, decimal_places=2, description="Total de la venta")


class VentaCreate(BaseModel):
    """
    Schema para crear una Venta completa (cabecera + detalles)
    
    NOTA: precio_total se calcula automáticamente mediante trigger.
    fecha tiene valor por defecto CURRENT_DATE si no se proporciona.
    """
    detalles: str = Field(..., max_length=200, description="Descripción de la venta")
    fecha: Optional[date] = Field(None, description="Fecha de la venta (opcional, default CURRENT_DATE)")
    detalles_venta: List[VentaDetalleCreate] = Field(
        ..., 
        min_length=1, 
        description="Lista de productos vendidos"
    )
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "detalles": "Venta de pastel y bebidas",
                "fecha": "2025-11-25",
                "detalles_venta": [
                    {
                        "id_producto": 1,
                        "cantidad": 1,
                        "precio": "380.00"
                    },
                    {
                        "id_producto": 15,
                        "cantidad": 2,
                        "precio": "45.00"
                    }
                ]
            }
        }
    )


class VentaUpdate(BaseModel):
    """
    Schema para actualizar una Venta - todos los campos opcionales
    
    NOTA: No se debe modificar precio_total manualmente, 
    se recalcula automáticamente por trigger.
    """
    detalles: Optional[str] = Field(None, max_length=200)
    fecha: Optional[date] = None


class VentaOut(VentaBase):
    """Schema para retornar una Venta con sus detalles"""
    id: int = Field(..., description="ID de la venta")
    detalles_venta: List[VentaDetalleOut] = Field(
        default_factory=list, 
        description="Lista de productos vendidos"
    )
    
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "detalles": "Venta de pastel y bebidas",
                "fecha": "2025-11-25",
                "precio_total": "470.00",
                "detalles_venta": [
                    {
                        "id": 1,
                        "id_venta": 1,
                        "id_producto": 1,
                        "cantidad": 1,
                        "precio": "380.00"
                    },
                    {
                        "id": 2,
                        "id_venta": 1,
                        "id_producto": 15,
                        "cantidad": 2,
                        "precio": "45.00"
                    }
                ]
            }
        }
    )


# ============================================
# SCHEMA PARA FUNCIÓN SQL insertar_venta()
# ============================================

class VentaDetalleJSON(BaseModel):
    """
    Schema para el formato JSON que espera la función insertar_venta()
    de PostgreSQL
    """
    id_producto: int = Field(..., description="ID del producto")
    cantidad: int = Field(..., ge=1, description="Cantidad")
    precio: Decimal = Field(..., ge=0, decimal_places=2, description="Precio unitario")


class InsertarVentaRequest(BaseModel):
    """
    Schema para llamar a la función SQL insertar_venta()
    """
    detalles: str = Field(..., max_length=200, description="Descripción de la venta")
    venta_detalle: List[VentaDetalleJSON] = Field(
        ..., 
        min_length=1,
        description="Array JSON de productos"
    )
    fecha: Optional[date] = Field(None, description="Fecha (opcional)")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "detalles": "Venta de pastel",
                "fecha": "2025-11-25",
                "venta_detalle": [
                    {"id_producto": 9, "cantidad": 10, "precio": "35.00"},
                    {"id_producto": 12, "cantidad": 6, "precio": "72.00"}
                ]
            }
        }
    )
