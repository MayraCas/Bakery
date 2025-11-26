
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import date
from decimal import Decimal



# VENTA DETALLE


class VentaDetalleBase(BaseModel):
    id_producto: Optional[int] = Field(None, description="ID del producto vendido")
    cantidad: Optional[int] = Field(None, ge=1, description="Cantidad vendida")
    precio: Optional[Decimal] = Field(None, ge=0, decimal_places=2, description="Precio unitario")


class VentaDetalleCreate(VentaDetalleBase):

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
    id_producto: Optional[int] = Field(None, description="ID del producto vendido")
    cantidad: Optional[int] = Field(None, ge=1)
    precio: Optional[Decimal] = Field(None, ge=0, decimal_places=2)


class VentaDetalleOut(VentaDetalleBase):
    id: int = Field(..., description="ID del detalle")
    id_venta: int = Field(..., description="ID de la venta")
    
    model_config = ConfigDict(from_attributes=True)




class VentaBase(BaseModel):
    detalles: Optional[str] = Field(None, max_length=200, description="Descripción de la venta")
    fecha: Optional[date] = Field(None, description="Fecha de la venta")
    precio_total: Optional[Decimal] = Field(None, ge=0, decimal_places=2, description="Total de la venta")


class VentaCreate(BaseModel):

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

    detalles: Optional[str] = Field(None, max_length=200)
    fecha: Optional[date] = None


class VentaOut(VentaBase):
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



# SCHEMA PARA FUNCIÓN SQL


class VentaDetalleJSON(BaseModel):

    id_producto: int = Field(..., description="ID del producto")
    cantidad: int = Field(..., ge=1, description="Cantidad")
    precio: Decimal = Field(..., ge=0, decimal_places=2, description="Precio unitario")
    variante: str = Field(..., description="Variante del producto: small, medium, big, retail, wholesale")


class InsertarVentaRequest(BaseModel):

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
                    {"id_producto": 1, "cantidad": 1, "precio": "380.00", "variante": "medium"},
                    {"id_producto": 15, "cantidad": 2, "precio": "45.00", "variante": "small"}
                ]
            }
        }
    )
