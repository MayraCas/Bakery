from .producto import ProductoRepository
from .postre import PostreRepository
from .pan import PanRepository
from .bebida import BebidaRepository
from .extra import ExtraRepository
from .venta import VentaRepository, VentaDetalleRepository

__all__ = [
    "ProductoRepository",
    "PostreRepository",
    "PanRepository",
    "BebidaRepository",
    "ExtraRepository",
    "VentaRepository",
    "VentaDetalleRepository",
]
