
from pydantic import BaseModel, Field, ConfigDict, field_serializer, field_validator
from typing import Optional, List, Union
from app.models.types import TypeDessert
from .types import PriceSizeSchema, StatusSizeSchema
from decimal import Decimal


class PostreBase(BaseModel):
    nombre: Optional[str] = Field(None, max_length=50, description="Nombre del postre")
    descripcion: Optional[str] = Field(None, description="Descripción del postre")
    imagen_url: Optional[str] = Field(None, description="URL de la imagen")
    tipo_postre: Optional[TypeDessert] = Field(None, description="Tipo de postre")
    precio: Optional[Union[PriceSizeSchema, tuple]] = Field(None, description="Precio según tamaño")
    disponible: Optional[Union[StatusSizeSchema, tuple]] = Field(None, description="Disponibilidad según tamaño")
    ingredientes: Optional[List[str]] = Field(None, description="Lista de ingredientes")
    es_dulce: Optional[bool] = Field(None, description="Indica si es dulce")


class PostreCreate(PostreBase):
    nombre: str = Field(..., max_length=50, description="Nombre del postre")
    tipo_postre: TypeDessert = Field(..., description="Tipo de postre")
    precio: PriceSizeSchema = Field(..., description="Precio según tamaño")
    ingredientes: List[str] = Field(..., min_length=1, description="Lista de ingredientes")
    es_dulce: bool = Field(..., description="Indica si es dulce")


class PostreUpdate(BaseModel):
    nombre: Optional[str] = Field(None, max_length=50)
    descripcion: Optional[str] = None
    imagen_url: Optional[str] = None
    tipo_postre: Optional[TypeDessert] = None
    precio: Optional[PriceSizeSchema] = None
    disponible: Optional[StatusSizeSchema] = None
    ingredientes: Optional[List[str]] = None
    es_dulce: Optional[bool] = None


class PostreOut(PostreBase):
    id: int = Field(..., description="ID del postre")
    
    @field_validator('precio', mode='before')
    @classmethod
    def convert_precio_tuple(cls, v):
        if v is None:
            return None
        
        if isinstance(v, str):
            cleaned = v.strip('()')
            parts = cleaned.split(',')
            if len(parts) == 3:
                return PriceSizeSchema(
                    small=Decimal(parts[0]),
                    medium=Decimal(parts[1]),
                    big=Decimal(parts[2])
                )
        
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
        if v is None:
            return StatusSizeSchema(small=True, medium=True, big=True)
        
        if isinstance(v, str):
            cleaned = v.strip('()')
            parts = cleaned.split(',')
            if len(parts) == 3:
                return StatusSizeSchema(
                    small=parts[0].lower() == 't',
                    medium=parts[1].lower() == 't',
                    big=parts[2].lower() == 't'
                )
        
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
                "id": 1,
                "nombre": "Pastel de Tres Leches",
                "descripcion": "Clásico pastel humedecido en tres leches",
                "tipo_postre": "Pastel",
                "precio": {
                    "small": "250.00",
                    "medium": "380.00",
                    "big": "500.00"
                },
                "ingredientes": ["Leche", "Leche condensada", "Harina", "Huevo"],
                "es_dulce": True,
                "imagen_url": "https://example.com/pastel.jpg"
            }
        }
    )
