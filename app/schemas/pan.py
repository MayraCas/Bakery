
from pydantic import BaseModel, Field, ConfigDict, field_validator
from typing import Optional, List, Union
from app.models.types import TypeBread
from .types import PriceAmountSchema
from decimal import Decimal


class PanBase(BaseModel):
    nombre: Optional[str] = Field(None, max_length=50, description="Nombre del pan")
    descripcion: Optional[str] = Field(None, description="Descripción del pan")
    imagen_url: Optional[str] = Field(None, description="URL de la imagen")
    tipo_pan: Optional[TypeBread] = Field(None, description="Tipo de pan")
    precio: Optional[Union[PriceAmountSchema, tuple]] = Field(None, description="Precio según cantidad")
    disponible: Optional[bool] = Field(None, description="Disponibilidad del producto")
    ingredientes: Optional[List[str]] = Field(None, description="Lista de ingredientes")


class PanCreate(PanBase):
    nombre: str = Field(..., max_length=50, description="Nombre del pan")
    tipo_pan: TypeBread = Field(..., description="Tipo de pan")
    precio: PriceAmountSchema = Field(..., description="Precio según cantidad")
    ingredientes: List[str] = Field(..., min_length=1, description="Lista de ingredientes")


class PanUpdate(BaseModel):
    nombre: Optional[str] = Field(None, max_length=50)
    descripcion: Optional[str] = None
    imagen_url: Optional[str] = None
    tipo_pan: Optional[TypeBread] = None
    precio: Optional[PriceAmountSchema] = None
    disponible: Optional[bool] = None
    ingredientes: Optional[List[str]] = None


class PanOut(PanBase):
    id: int = Field(..., description="ID del pan")
    
    @field_validator('precio', mode='before')
    @classmethod
    def convert_precio_tuple(cls, v):
        if v is None:
            return None
        
        if isinstance(v, str):
            cleaned = v.strip('()')
            parts = cleaned.split(',')
            if len(parts) == 2:
                return PriceAmountSchema(
                    retail_sale=Decimal(parts[0]),
                    wholesale=Decimal(parts[1])
                )
        
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
                "id": 9,
                "nombre": "Bolillo Tradicional",
                "descripcion": "Pan blanco crujiente por fuera",
                "tipo_pan": "Salado",
                "precio": {
                    "retail_sale": "5.00",
                    "wholesale": "3.50"
                },
                "ingredientes": ["Harina", "Levadura", "Sal", "Agua"],
                "imagen_url": "https://example.com/bolillo.jpg"
            }
        }
    )
