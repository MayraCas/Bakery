"""
Schemas Pydantic para Extra (hereda de Producto)
"""
from pydantic import BaseModel, Field, ConfigDict, field_validator
from typing import Optional, Union
from app.models.types import TypeExtra
from .types import PriceAmountSchema
from decimal import Decimal


class ExtraBase(BaseModel):
    """Schema base para Extra - atributos comunes"""
    nombre: Optional[str] = Field(None, max_length=50, description="Nombre del extra")
    descripcion: Optional[str] = Field(None, description="Descripción del extra")
    imagen_url: Optional[str] = Field(None, description="URL de la imagen")
    tipo_extra: Optional[TypeExtra] = Field(None, description="Tipo de extra")
    precio: Optional[Union[PriceAmountSchema, tuple]] = Field(None, description="Precio según cantidad")
    disponible: Optional[bool] = Field(None, description="Disponibilidad del producto")


class ExtraCreate(ExtraBase):
    """Schema para crear un Extra"""
    nombre: str = Field(..., max_length=50, description="Nombre del extra")
    tipo_extra: TypeExtra = Field(..., description="Tipo de extra")
    precio: PriceAmountSchema = Field(..., description="Precio según cantidad")


class ExtraUpdate(BaseModel):
    """Schema para actualizar un Extra - todos los campos opcionales"""
    nombre: Optional[str] = Field(None, max_length=50)
    descripcion: Optional[str] = None
    imagen_url: Optional[str] = None
    tipo_extra: Optional[TypeExtra] = None
    precio: Optional[PriceAmountSchema] = None
    disponible: Optional[bool] = None


class ExtraOut(ExtraBase):
    """Schema para retornar un Extra"""
    id: int = Field(..., description="ID del extra")
    
    @field_validator('precio', mode='before')
    @classmethod
    def convert_precio_tuple(cls, v):
        """Convierte tupla de PostgreSQL a PriceAmountSchema"""
        if v is None:
            return None
        
        # Si viene como string (formato PostgreSQL: '(5.00,3.50)')
        if isinstance(v, str):
            # Remover paréntesis y dividir por comas
            cleaned = v.strip('()')
            parts = cleaned.split(',')
            if len(parts) == 2:
                return PriceAmountSchema(
                    retail_sale=Decimal(parts[0]),
                    wholesale=Decimal(parts[1])
                )
        
        # Si viene como tupla de PostgreSQL, convertir a schema
        if isinstance(v, tuple) and len(v) == 2:
            return PriceAmountSchema(
                retail_sale=Decimal(str(v[0])),
                wholesale=Decimal(str(v[1]))
            )
        return v
    
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 21,
                "nombre": "Vela Mágica",
                "descripcion": "Vela de chispas para cumpleaños",
                "tipo_extra": "Vela",
                "precio": {
                    "retail_sale": "15.00",
                    "wholesale": "10.00"
                },
                "imagen_url": "https://example.com/vela.jpg"
            }
        }
    )
