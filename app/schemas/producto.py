
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional


class ProductoBase(BaseModel):
    nombre: Optional[str] = Field(None, max_length=50, description="Nombre del producto")
    descripcion: Optional[str] = Field(None, description="Descripción del producto")
    imagen_url: Optional[str] = Field(None, description="URL de la imagen del producto")


class ProductoCreate(ProductoBase):
    nombre: str = Field(..., max_length=50, description="Nombre del producto")
    imagen_url: str = Field(..., description="URL de la imagen del producto")


class ProductoUpdate(BaseModel):
    nombre: Optional[str] = Field(None, max_length=50)
    descripcion: Optional[str] = None
    imagen_url: Optional[str] = None


class ProductoOut(ProductoBase):
    id: int = Field(..., description="ID del producto")
    
    model_config = ConfigDict(from_attributes=True)
