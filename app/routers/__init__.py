"""
Routers - Endpoints de la API
"""
from .producto import router as producto_router
from .postre import router as postre_router
from .pan import router as pan_router
from .bebida import router as bebida_router
from .extra import router as extra_router
from .venta import router as venta_router

__all__ = [
    "producto_router",
    "postre_router",
    "pan_router",
    "bebida_router",
    "extra_router",
    "venta_router",
]
