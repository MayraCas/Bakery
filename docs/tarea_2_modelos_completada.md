# Tarea 2: Modelos SQLAlchemy - COMPLETADA ✅

## Estructura Creada

```
app/
├── __init__.py
├── database.py
└── models/
    ├── __init__.py
    ├── base.py
    ├── types.py
    ├── utils.py
    ├── producto.py (padre)
    ├── postre.py
    ├── pan.py
    ├── bebida.py
    ├── extra.py
    └── venta.py
```

## Archivos Implementados

### 1. `app/models/base.py`
- **DeclarativeBase** usando SQLAlchemy 2.0
- Base class para todos los modelos

### 2. `app/models/types.py`
- **Tipos Compuestos (NamedTuple)**:
  - `PriceSize(small, medium, big)` → para postre y bebida
  - `PriceAmount(retail_sale, wholesale)` → para pan y extra

- **Tipos Enumerados (Enum)**:
  - `TypeDessert`: 9 valores (Pastel, Tarta, Helado, etc.)
  - `TypeBread`: 2 valores (Dulce, Salado)
  - `TypeDrink`: 6 valores (Batido, Smoothie, Frappé, etc.)
  - `TypeExtra`: 5 valores (Vela, Molde, Plato, etc.)

### 3. `app/models/producto.py` (Tabla Padre)
- **Herencia**: Usa `polymorphic_identity` para joined-table inheritance
- **Columnas**:
  - `id`: SERIAL PRIMARY KEY
  - `nombre`: VARCHAR(50)
  - `descripcion`: VARCHAR(100)
  - `cantidad`: INTEGER (stock)
  - `imagen_url`: TEXT

### 4. Modelos Hijos con Herencia

#### `app/models/postre.py`
- Hereda de `Producto`
- **Columnas adicionales**:
  - `tipo_postre`: ENUM type_dessert
  - `precio`: Composite type (price_size) → tupla
  - `ingredientes`: ARRAY de TEXT
  - `es_dulce`: BOOLEAN
- **FK**: `id` → `producto.id`

#### `app/models/pan.py`
- Hereda de `Producto`
- **Columnas adicionales**:
  - `tipo_pan`: ENUM type_bread
  - `precio`: Composite type (price_amount) → tupla
  - `ingredientes`: ARRAY de TEXT
- **FK**: `id` → `producto.id`

#### `app/models/bebida.py`
- Hereda de `Producto`
- **Columnas adicionales**:
  - `tipo_bebida`: ENUM type_drink
  - `precio`: Composite type (price_size) → tupla
  - `ingredientes`: ARRAY de TEXT
  - `es_fria`: BOOLEAN
- **FK**: `id` → `producto.id`

#### `app/models/extra.py`
- Hereda de `Producto`
- **Columnas adicionales**:
  - `tipo_extra`: ENUM type_extra
  - `precio`: Composite type (price_amount) → tupla
- **FK**: `id` → `producto.id`

### 5. `app/models/venta.py`
Contiene dos modelos:

#### `Venta`
- **Columnas**:
  - `id`: SERIAL PRIMARY KEY
  - `detalles`: VARCHAR(200)
  - `fecha`: DATE (default CURRENT_DATE)
  - `precio_total`: NUMERIC(10,2)
- **Relación**: uno a muchos con `VentaDetalle`

#### `VentaDetalle`
- **Columnas**:
  - `id`: SERIAL PRIMARY KEY
  - `id_venta`: INTEGER FK → venta(id) ON DELETE CASCADE
  - `id_producto`: INTEGER (SIN FK explícita)
  - `cantidad`: INTEGER
  - `precio`: NUMERIC(10,2)
- **Relación**: muchos a uno con `Venta`
- **NOTA IMPORTANTE**: `id_producto` NO tiene FK debido a la herencia. La integridad se valida mediante trigger en PostgreSQL.

### 6. `app/models/utils.py`
Utilidades para convertir tipos compuestos:
- `tuple_to_price_size()` - Convierte tupla PostgreSQL a PriceSize
- `tuple_to_price_amount()` - Convierte tupla PostgreSQL a PriceAmount
- `price_size_to_tuple()` - Convierte PriceSize a tupla para insert
- `price_amount_to_tuple()` - Convierte PriceAmount a tupla para insert

### 7. `app/database.py`
- Engine de SQLAlchemy 2.0
- SessionLocal factory
- Función `get_db()` para dependency injection en FastAPI

## Características Técnicas Implementadas

### ✅ Herencia Joined-Table
```python
# Producto (padre)
__mapper_args__ = {
    "polymorphic_identity": "producto",
    "with_polymorphic": "*",
}

# Postre (hijo)
id = mapped_column(Integer, ForeignKey("producto.id"), primary_key=True)
__mapper_args__ = {
    "polymorphic_identity": "postre",
}
```

### ✅ Tipos Compuestos PostgreSQL
- Los tipos compuestos `price_size` y `price_amount` se mapean como `Column` genérico
- PostgreSQL los devuelve como tuplas
- Las utilidades convierten entre tuplas y NamedTuples tipados

### ✅ Arrays PostgreSQL
```python
ingredientes: Mapped[List[str] | None] = mapped_column(
    ARRAY(item_type=str),
    nullable=True
)
```

### ✅ ENUM Types
```python
tipo_postre: Mapped[TypeDessert | None] = mapped_column(
    SQLEnum(TypeDessert, name="type_dessert", create_type=False),
    nullable=True
)
```
- `create_type=False` porque los ENUMs ya existen en la BD

### ✅ Relationships
```python
# Venta → VentaDetalle (1:N)
detalles_venta: Mapped[List["VentaDetalle"]] = relationship(
    "VentaDetalle",
    back_populates="venta",
    cascade="all, delete-orphan"
)
```

## Verificación

Se creó `test_models.py` que verifica:
- ✅ Importación correcta de todos los modelos
- ✅ Estructura de herencia
- ✅ Tipos compuestos (PriceSize, PriceAmount)
- ✅ Tipos ENUM con sus valores
- ✅ Relaciones entre Venta y VentaDetalle

**Resultado**: ✅ TODOS LOS MODELOS SE IMPORTARON CORRECTAMENTE

## Decisiones de Diseño

1. **Joined-Table Inheritance**: Elegido porque representa fielmente la herencia nativa de PostgreSQL con `INHERITS`.

2. **Tipos Compuestos como Column genérico**: SQLAlchemy 2.0 no tiene soporte completo para `COMPOSITE` types de PostgreSQL. Se usan `Column` sin tipo y se procesan en la capa de aplicación.

3. **ENUMs sin crear**: `create_type=False` porque los ENUMs ya están definidos en la base de datos SQL.

4. **Sin FK en id_producto**: Respeta la implementación de la BD donde la FK se valida mediante trigger por la herencia.

5. **SQLAlchemy 2.0 Style**: Uso de `DeclarativeBase`, `Mapped[]`, `mapped_column()` siguiendo las mejores prácticas de SQLAlchemy 2.0.

## Siguiente Paso

**Tarea 3**: Crear los Schemas Pydantic
