"""
Schemas Pydantic para validación y serialización
"""
from .types import PriceSizeSchema, PriceAmountSchema
from .producto import ProductoBase, ProductoCreate, ProductoUpdate, ProductoOut
from .postre import PostreBase, PostreCreate, PostreUpdate, PostreOut
from .pan import PanBase, PanCreate, PanUpdate, PanOut
from .bebida import BebidaBase, BebidaCreate, BebidaUpdate, BebidaOut
from .extra import ExtraBase, ExtraCreate, ExtraUpdate, ExtraOut
from .venta import (
    VentaBase,
    VentaCreate,
    VentaUpdate,
    VentaOut,
    VentaDetalleBase,
    VentaDetalleCreate,
    VentaDetalleUpdate,
    VentaDetalleOut,
    InsertarVentaRequest,
    VentaDetalleJSON,
)

__all__ = [
    # Types
    "PriceSizeSchema",
    "PriceAmountSchema",
    # Producto
    "ProductoBase",
    "ProductoCreate",
    "ProductoUpdate",
    "ProductoOut",
    # Postre
    "PostreBase",
    "PostreCreate",
    "PostreUpdate",
    "PostreOut",
    # Pan
    "PanBase",
    "PanCreate",
    "PanUpdate",
    "PanOut",
    # Bebida
    "BebidaBase",
    "BebidaCreate",
    "BebidaUpdate",
    "BebidaOut",
    # Extra
    "ExtraBase",
    "ExtraCreate",
    "ExtraUpdate",
    "ExtraOut",
    # Venta
    "VentaBase",
    "VentaCreate",
    "VentaUpdate",
    "VentaOut",
    "VentaDetalleBase",
    "VentaDetalleCreate",
    "VentaDetalleUpdate",
    "VentaDetalleOut",
    "InsertarVentaRequest",
    "VentaDetalleJSON",
]
