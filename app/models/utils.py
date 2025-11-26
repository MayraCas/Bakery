"""
Utilidades para manejar tipos compuestos de PostgreSQL
SQLAlchemy no tiene soporte nativo completo para composite types,
por lo que estas funciones ayudan a convertir entre tuplas y objetos Python.
"""
from typing import Tuple, Optional
from decimal import Decimal
from .types import PriceSize, PriceAmount


def tuple_to_price_size(value: Optional[Tuple]) -> Optional[PriceSize]:
    """
    Convierte una tupla de PostgreSQL price_size a objeto PriceSize.
    
    Args:
        value: Tupla (small, medium, big) o None
        
    Returns:
        PriceSize NamedTuple o None
    """
    if value is None:
        return None
    if isinstance(value, tuple) and len(value) == 3:
        return PriceSize(
            small=Decimal(str(value[0])) if value[0] is not None else Decimal('0'),
            medium=Decimal(str(value[1])) if value[1] is not None else Decimal('0'),
            big=Decimal(str(value[2])) if value[2] is not None else Decimal('0')
        )
    return None


def tuple_to_price_amount(value: Optional[Tuple]) -> Optional[PriceAmount]:
    """
    Convierte una tupla de PostgreSQL price_amount a objeto PriceAmount.
    
    Args:
        value: Tupla (retail_sale, wholesale) o None
        
    Returns:
        PriceAmount NamedTuple o None
    """
    if value is None:
        return None
    if isinstance(value, tuple) and len(value) == 2:
        return PriceAmount(
            retail_sale=Decimal(str(value[0])) if value[0] is not None else Decimal('0'),
            wholesale=Decimal(str(value[1])) if value[1] is not None else Decimal('0')
        )
    return None


def price_size_to_tuple(price: Optional[PriceSize]) -> Optional[Tuple[Decimal, Decimal, Decimal]]:
    """
    Convierte un objeto PriceSize a tupla para inserción en PostgreSQL.
    
    Args:
        price: Objeto PriceSize o None
        
    Returns:
        Tupla (small, medium, big) o None
    """
    if price is None:
        return None
    return (price.small, price.medium, price.big)


def price_amount_to_tuple(price: Optional[PriceAmount]) -> Optional[Tuple[Decimal, Decimal]]:
    """
    Convierte un objeto PriceAmount a tupla para inserción en PostgreSQL.
    
    Args:
        price: Objeto PriceAmount o None
        
    Returns:
        Tupla (retail_sale, wholesale) o None
    """
    if price is None:
        return None
    return (price.retail_sale, price.wholesale)
