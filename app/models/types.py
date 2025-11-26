"""
Tipos personalizados que mapean tipos compuestos de PostgreSQL
"""
from typing import NamedTuple
from decimal import Decimal
import enum


# ============================================
# TIPOS COMPUESTOS (Composite Types)
# ============================================

class PriceSize(NamedTuple):
    """
    Mapea el tipo compuesto PostgreSQL: price_size
    Representa precio según tamaño (pequeño, mediano, grande)
    """
    small: Decimal
    medium: Decimal
    big: Decimal


class PriceAmount(NamedTuple):
    """
    Mapea el tipo compuesto PostgreSQL: price_amount
    Representa precio según cantidad (al por menor, al por mayor)
    """
    retail_sale: Decimal  # AL POR MENOR
    wholesale: Decimal    # AL POR MAYOR


# ============================================
# TIPOS ENUMERADOS (ENUM Types)
# ============================================

class TypeDessert(str, enum.Enum):
    """Tipo de postre"""
    PASTEL = "Pastel"
    TARTA = "Tarta"
    HELADO = "Helado"
    PUDIN = "Pudín"
    FLAN = "Flan"
    GELATINA = "Gelatina"
    GALLETA = "Galleta"
    MOUSSES = "Mousses"
    CREPA = "Crepa"


class TypeBread(str, enum.Enum):
    """Tipo de pan"""
    DULCE = "Dulce"
    SALADO = "Salado"


class TypeDrink(str, enum.Enum):
    """Tipo de bebida"""
    BATIDO = "Batido"
    SMOOTHIE = "Smoothie"
    FRAPPE = "Frappé"
    LICUADO = "Licuado"
    MALTEADA = "Malteada"
    CAFE = "Café"


class TypeExtra(str, enum.Enum):
    """Tipo de extra"""
    VELA = "Vela"
    MOLDE = "Molde"
    PLATO = "Plato"
    VASO = "Vaso"
    CHAROLA = "Charola"
