from pydantic import BaseModel
from typing import Optional, List

class PostreSchema(BaseModel):
    nombre: str
    descripcion: Optional[str]
    precio: float
    cantidad: int
    tipo_postre: str
    ingredientes: List[str]
    es_dulce: bool