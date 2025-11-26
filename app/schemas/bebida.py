"""
Schemas Pydantic para Bebida (hereda de Producto)
"""
from pydantic import BaseModel, Field, ConfigDict, field_validator
from typing import Optional, List, Union
from app.models.types import TypeDrink
from .types import PriceSizeSchema, StatusSizeSchema
from decimal import Decimal


class BebidaBase(BaseModel):
    """Schema base para Bebida - atributos comunes"""
    nombre: Optional[str] = Field(None, max_length=50, description="Nombre de la bebida")
    descripcion: Optional[str] = Field(None, description="Descripción de la bebida")
    imagen_url: Optional[str] = Field(None, description="URL de la imagen")
    tipo_bebida: Optional[TypeDrink] = Field(None, description="Tipo de bebida")
    precio: Optional[Union[PriceSizeSchema, tuple]] = Field(None, description="Precio según tamaño")
    disponible: Optional[Union[StatusSizeSchema, tuple]] = Field(None, description="Disponibilidad según tamaño")
    ingredientes: Optional[List[str]] = Field(None, description="Lista de ingredientes")
    es_fria: Optional[bool] = Field(None, description="Indica si es fría")


class BebidaCreate(BebidaBase):
    """Schema para crear una Bebida"""
    nombre: str = Field(..., max_length=50, description="Nombre de la bebida")
    tipo_bebida: TypeDrink = Field(..., description="Tipo de bebida")
    precio: PriceSizeSchema = Field(..., description="Precio según tamaño")
    ingredientes: List[str] = Field(..., min_length=1, description="Lista de ingredientes")
    es_fria: bool = Field(..., description="Indica si es fría")


class BebidaUpdate(BaseModel):
    """Schema para actualizar una Bebida - todos los campos opcionales"""
    nombre: Optional[str] = Field(None, max_length=50)
    descripcion: Optional[str] = None
    imagen_url: Optional[str] = None
    tipo_bebida: Optional[TypeDrink] = None
    precio: Optional[PriceSizeSchema] = None
    disponible: Optional[StatusSizeSchema] = None
    ingredientes: Optional[List[str]] = None
    es_fria: Optional[bool] = None


class BebidaOut(BebidaBase):
    """Schema para retornar una Bebida"""
    id: int = Field(..., description="ID de la bebida")
    
    @field_validator('precio', mode='before')
    @classmethod
    def convert_precio_tuple(cls, v):
        """Convierte tupla de PostgreSQL a PriceSizeSchema"""
        if v is None:
            return None
        
        # Si viene como string (formato PostgreSQL: '(250.00,450.00,600.00)')
        if isinstance(v, str):
            # Remover paréntesis y dividir por comas
            cleaned = v.strip('()')
            parts = cleaned.split(',')
            if len(parts) == 3:
                return PriceSizeSchema(
                    small=Decimal(parts[0]),
                    medium=Decimal(parts[1]),
                    big=Decimal(parts[2])
                )
        
        # Si viene como tupla de PostgreSQL, convertir a schema
        if isinstance(v, tuple) and len(v) == 3:
            return PriceSizeSchema(
                small=Decimal(str(v[0])),
                medium=Decimal(str(v[1])),
                big=Decimal(str(v[2]))
            )
        return v
    
    @field_validator('disponible', mode='before')
    @classmethod
    def convert_disponible_tuple(cls, v):
        """Convierte tupla de PostgreSQL a StatusSizeSchema"""
        if v is None:
            return StatusSizeSchema(small=True, medium=True, big=True)
        
        # Si viene como string (formato PostgreSQL: '(t,t,f)')
        if isinstance(v, str):
            cleaned = v.strip('()')
            parts = cleaned.split(',')
            if len(parts) == 3:
                return StatusSizeSchema(
                    small=parts[0].lower() == 't',
                    medium=parts[1].lower() == 't',
                    big=parts[2].lower() == 't'
                )
        
        # Si viene como tupla de PostgreSQL
        if isinstance(v, tuple) and len(v) == 3:
            return StatusSizeSchema(
                small=bool(v[0]),
                medium=bool(v[1]),
                big=bool(v[2])
            )
        return v
    
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 15,
                "nombre": "Licuado de Fresa",
                "descripcion": "Licuado con leche entera",
                "tipo_bebida": "Licuado",
                "precio": {
                    "small": "35.00",
                    "medium": "45.00",
                    "big": "55.00"
                },
                "ingredientes": ["Leche", "Fresa", "Azúcar"],
                "es_fria": True,
                "imagen_url": "https://example.com/licuado.jpg"
            }
        }
    )
