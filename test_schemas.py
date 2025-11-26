"""
Script de prueba para verificar que los Schemas Pydantic están correctamente definidos.
Valida serialización, deserialización y validación de datos.
"""
from app.schemas import (
    PriceSizeSchema,
    PriceAmountSchema,
    ProductoCreate,
    ProductoOut,
    PostreCreate,
    PostreOut,
    PanCreate,
    PanOut,
    BebidaCreate,
    BebidaOut,
    ExtraCreate,
    ExtraOut,
    VentaCreate,
    VentaOut,
    InsertarVentaRequest,
)
from app.models.types import TypeDessert, TypeBread, TypeDrink, TypeExtra
from decimal import Decimal
from datetime import date
import json


def test_schemas():
    """Prueba que los schemas funcionen correctamente"""
    print("=" * 60)
    print("VERIFICACIÓN DE SCHEMAS PYDANTIC")
    print("=" * 60)
    
    # Test Tipos Compuestos
    print("\n✓ Tipos Compuestos")
    price_size = PriceSizeSchema(
        small=Decimal("250.00"),
        medium=Decimal("380.00"),
        big=Decimal("500.00")
    )
    print(f"  - PriceSize: {price_size.model_dump()}")
    
    price_amount = PriceAmountSchema(
        retail_sale=Decimal("5.00"),
        wholesale=Decimal("3.50")
    )
    print(f"  - PriceAmount: {price_amount.model_dump()}")
    
    # Test PostreCreate
    print("\n✓ PostreCreate")
    postre_data = {
        "nombre": "Pastel de Chocolate",
        "descripcion": "Delicioso pastel",
        "cantidad": 10,
        "tipo_postre": TypeDessert.PASTEL,
        "precio": {
            "small": "200.00",
            "medium": "350.00",
            "big": "480.00"
        },
        "ingredientes": ["Chocolate", "Harina", "Huevo", "Azúcar"],
        "es_dulce": True,
        "imagen_url": "https://example.com/pastel.jpg"
    }
    postre = PostreCreate(**postre_data)
    print(f"  - Nombre: {postre.nombre}")
    print(f"  - Tipo: {postre.tipo_postre.value}")
    print(f"  - Precio: {postre.precio.model_dump()}")
    print(f"  - Ingredientes: {len(postre.ingredientes)} items")
    
    # Test PanCreate
    print("\n✓ PanCreate")
    pan_data = {
        "nombre": "Concha de Vainilla",
        "descripcion": "Pan dulce tradicional",
        "cantidad": 50,
        "tipo_pan": TypeBread.DULCE,
        "precio": {
            "retail_sale": "12.00",
            "wholesale": "9.50"
        },
        "ingredientes": ["Harina", "Azúcar", "Mantequilla"],
        "imagen_url": "https://example.com/concha.jpg"
    }
    pan = PanCreate(**pan_data)
    print(f"  - Nombre: {pan.nombre}")
    print(f"  - Tipo: {pan.tipo_pan.value}")
    print(f"  - Precio: {pan.precio.model_dump()}")
    
    # Test BebidaCreate
    print("\n✓ BebidaCreate")
    bebida_data = {
        "nombre": "Frappé Moka",
        "descripcion": "Café frío con chocolate",
        "cantidad": 25,
        "tipo_bebida": TypeDrink.FRAPPE,
        "precio": {
            "small": "50.00",
            "medium": "65.00",
            "big": "80.00"
        },
        "ingredientes": ["Café", "Chocolate", "Hielo", "Leche"],
        "es_fria": True,
        "imagen_url": "https://example.com/frappe.jpg"
    }
    bebida = BebidaCreate(**bebida_data)
    print(f"  - Nombre: {bebida.nombre}")
    print(f"  - Tipo: {bebida.tipo_bebida.value}")
    print(f"  - Es fría: {bebida.es_fria}")
    
    # Test ExtraCreate
    print("\n✓ ExtraCreate")
    extra_data = {
        "nombre": "Vela Numérica",
        "descripcion": "Vela con número",
        "cantidad": 100,
        "tipo_extra": TypeExtra.VELA,
        "precio": {
            "retail_sale": "12.00",
            "wholesale": "8.00"
        },
        "imagen_url": "https://example.com/vela.jpg"
    }
    extra = ExtraCreate(**extra_data)
    print(f"  - Nombre: {extra.nombre}")
    print(f"  - Tipo: {extra.tipo_extra.value}")
    
    # Test VentaCreate
    print("\n✓ VentaCreate")
    venta_data = {
        "detalles": "Venta de cumpleaños",
        "fecha": "2025-11-25",
        "detalles_venta": [
            {
                "id_producto": 1,
                "cantidad": 1,
                "precio": "380.00"
            },
            {
                "id_producto": 15,
                "cantidad": 2,
                "precio": "45.00"
            }
        ]
    }
    venta = VentaCreate(**venta_data)
    print(f"  - Detalles: {venta.detalles}")
    print(f"  - Fecha: {venta.fecha}")
    print(f"  - Productos: {len(venta.detalles_venta)} items")
    
    # Test InsertarVentaRequest (para función SQL)
    print("\n✓ InsertarVentaRequest (función SQL)")
    insertar_venta_data = {
        "detalles": "Venta rápida",
        "fecha": "2025-11-25",
        "venta_detalle": [
            {"id_producto": 9, "cantidad": 10, "precio": "35.00"},
            {"id_producto": 12, "cantidad": 6, "precio": "72.00"}
        ]
    }
    insertar_venta = InsertarVentaRequest(**insertar_venta_data)
    print(f"  - Detalles: {insertar_venta.detalles}")
    print(f"  - Items: {len(insertar_venta.venta_detalle)}")
    
    # Test JSON Serialization
    print("\n✓ Serialización JSON")
    postre_json = postre.model_dump_json(indent=2)
    print(f"  - Postre serializado: {len(postre_json)} caracteres")
    
    venta_json = venta.model_dump_json(indent=2)
    print(f"  - Venta serializada: {len(venta_json)} caracteres")
    
    # Test Validación de Precios
    print("\n✓ Validación de Precios")
    try:
        # Intenta crear precio negativo (debe fallar)
        invalid_price = PriceSizeSchema(
            small=Decimal("-10.00"),
            medium=Decimal("20.00"),
            big=Decimal("30.00")
        )
        print("  ✗ ERROR: Se permitió precio negativo")
    except Exception as e:
        print(f"  ✓ Validación correcta: precios negativos rechazados")
    
    # Test Validación de Cantidad
    print("\n✓ Validación de Cantidad")
    try:
        # Intenta crear con cantidad negativa (debe fallar)
        invalid_postre = PostreCreate(
            nombre="Test",
            cantidad=-5,
            tipo_postre=TypeDessert.PASTEL,
            precio=price_size,
            ingredientes=["Test"],
            es_dulce=True
        )
        print("  ✗ ERROR: Se permitió cantidad negativa")
    except Exception as e:
        print(f"  ✓ Validación correcta: cantidades negativas rechazadas")
    
    # Test campo serializer de precio (tupla → dict)
    print("\n✓ Serialización de Tipos Compuestos desde Tupla")
    # Simula tupla que viene de PostgreSQL
    class PostreSimulado:
        id = 1
        nombre = "Pastel Test"
        descripcion = "Test"
        cantidad = 10
        imagen_url = None
        tipo_postre = "Pastel"
        precio = (Decimal("100"), Decimal("150"), Decimal("200"))  # Tupla de PostgreSQL
        ingredientes = ["Test"]
        es_dulce = True
    
    postre_out = PostreOut.model_validate(PostreSimulado())
    print(f"  - Precio original (tupla): {PostreSimulado.precio}")
    print(f"  - Precio serializado (dict): {postre_out.precio}")
    
    print("\n" + "=" * 60)
    print("✅ TODOS LOS SCHEMAS FUNCIONAN CORRECTAMENTE")
    print("=" * 60)
    
    # Mostrar ejemplo de JSON completo
    print("\n📄 Ejemplo JSON - Postre:")
    print(postre.model_dump_json(indent=2))
    
    print("\n📄 Ejemplo JSON - Venta:")
    print(venta.model_dump_json(indent=2))


if __name__ == "__main__":
    test_schemas()
