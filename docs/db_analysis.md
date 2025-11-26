# Análisis de la Base de Datos - Bakery System

## 1. Árbol de Herencia

```
producto (TABLA PADRE)
├── postre (INHERITS producto)
├── pan (INHERITS producto)
├── bebida (INHERITS producto)
└── extra (INHERITS producto)
```

**Mecanismo de Herencia:**
- PostgreSQL usa **herencia nativa** mediante `INHERITS`.
- Cada tabla hija contiene automáticamente todas las columnas del padre.
- Los registros insertados en las tablas hijas **NO** aparecen automáticamente en la tabla padre.
- Para consultar todos los productos (padre + hijos), se usa: `SELECT * FROM ONLY producto` o `SELECT * FROM producto*`.

---

## 2. Tipos Compuestos (Composite Types)

### 2.1 `price_size`
```sql
CREATE TYPE price_size AS (
    small NUMERIC(10,2),
    medium NUMERIC(10,2),
    big NUMERIC(10,2)
);
```
**Uso:** Almacena precios según tamaño del producto (pequeño, mediano, grande).

**Aplicado en:**
- `postre.precio`
- `bebida.precio`

**Ejemplo de valor:**
```sql
(250.00, 380.00, 500.00)
```

### 2.2 `price_amount`
```sql
CREATE TYPE price_amount AS (
    retail_sale NUMERIC(10,2),  -- AL POR MENOR
    wholesale NUMERIC(10,2)     -- AL POR MAYOR
);
```
**Uso:** Almacena precios según cantidad (venta al por menor vs mayoreo).

**Aplicado en:**
- `pan.precio`
- `extra.precio`

**Ejemplo de valor:**
```sql
(5.00, 3.50)
```

---

## 3. Tipos Enumerados (ENUM Types)

### 3.1 `type_dessert`
```sql
CREATE TYPE type_dessert AS ENUM(
    'Pastel', 'Tarta', 'Helado', 'Pudín', 'Flan', 
    'Gelatina', 'Galleta', 'Mousses', 'Crepa'
);
```

### 3.2 `type_bread`
```sql
CREATE TYPE type_bread AS ENUM('Dulce', 'Salado');
```

### 3.3 `type_drink`
```sql
CREATE TYPE type_drink AS ENUM(
    'Batido', 'Smoothie', 'Frappé', 'Licuado', 'Malteada', 'Café'
);
```

### 3.4 `type_extra`
```sql
CREATE TYPE type_extra AS ENUM(
    'Vela', 'Molde', 'Plato', 'Vaso', 'Charola'
);
```

---

## 4. Estructura de Tablas

### 4.1 Tabla Padre: `producto`

| Columna        | Tipo         | Restricción  |
|----------------|--------------|--------------|
| `id`           | SERIAL       | PRIMARY KEY  |
| `nombre`       | VARCHAR(50)  |              |
| `descripcion`  | VARCHAR(100) |              |
| `cantidad`     | INTEGER      |              |
| `imagen_url`   | TEXT         |              |

**Características:**
- Es la tabla base que contiene atributos comunes.
- `id` se genera automáticamente con SERIAL.
- `cantidad` representa el stock/inventario disponible.

---

### 4.2 Tabla Hija: `postre`

| Columna adicional | Tipo             |
|-------------------|------------------|
| `tipo_postre`     | type_dessert     |
| `precio`          | price_size       |
| `ingredientes`    | TEXT[]           |
| `es_dulce`        | BOOLEAN          |

**Hereda de:** `producto`

**Total de columnas:** 9 (5 del padre + 4 propias)

---

### 4.3 Tabla Hija: `pan`

| Columna adicional | Tipo             |
|-------------------|------------------|
| `tipo_pan`        | type_bread       |
| `precio`          | price_amount     |
| `ingredientes`    | TEXT[]           |

**Hereda de:** `producto`

**Total de columnas:** 8 (5 del padre + 3 propias)

---

### 4.4 Tabla Hija: `bebida`

| Columna adicional | Tipo             |
|-------------------|------------------|
| `tipo_bebida`     | type_drink       |
| `precio`          | price_size       |
| `ingredientes`    | TEXT[]           |
| `es_fria`         | BOOLEAN          |

**Hereda de:** `producto`

**Total de columnas:** 9 (5 del padre + 4 propias)

---

### 4.5 Tabla Hija: `extra`

| Columna adicional | Tipo             |
|-------------------|------------------|
| `tipo_extra`      | type_extra       |
| `precio`          | price_amount     |

**Hereda de:** `producto`

**Total de columnas:** 7 (5 del padre + 2 propias)

---

### 4.6 Tabla: `venta`

| Columna        | Tipo            | Restricción       |
|----------------|-----------------|-------------------|
| `id`           | SERIAL          | PRIMARY KEY       |
| `detalles`     | VARCHAR(200)    |                   |
| `fecha`        | DATE            | DEFAULT CURRENT_DATE |
| `precio_total` | NUMERIC(10,2)   |                   |

**Características:**
- Representa la cabecera de una venta.
- `precio_total` se calcula automáticamente mediante trigger.
- `fecha` se establece automáticamente a la fecha actual si no se proporciona.

---

### 4.7 Tabla: `venta_detalle`

| Columna        | Tipo            | Restricción                           |
|----------------|-----------------|---------------------------------------|
| `id`           | SERIAL          | PRIMARY KEY                           |
| `id_venta`     | INTEGER         | FK → `venta(id)` ON DELETE CASCADE    |
| `id_producto`  | INTEGER         | **NO HAY FK EXPLÍCITA**               |
| `cantidad`     | INTEGER         |                                       |
| `precio`       | NUMERIC(10,2)   |                                       |

**Características importantes:**
- **NO existe foreign key explícita** hacia `producto`.
- La integridad referencial se implementa mediante un **TRIGGER** (`trg_verificar_producto_fk`).
- Representa los productos individuales dentro de una venta.
- `precio` es el precio unitario del producto al momento de la venta.

---

## 5. Relación entre `venta` y `venta_detalle`

**Tipo de relación:** Uno a Muchos (1:N)

```
venta (1)
  │
  └──< venta_detalle (N)
```

**Flujo de trabajo:**
1. Se crea una venta en la tabla `venta`.
2. Se insertan múltiples productos en `venta_detalle` referenciando `id_venta`.
3. El trigger `trg_calcular_total_venta` suma automáticamente `cantidad * precio` de todos los detalles y actualiza `venta.precio_total`.

**Restricciones:**
- Si se elimina una venta (`DELETE FROM venta`), se eliminan en cascada todos sus detalles (`ON DELETE CASCADE`).

---

## 6. Triggers Implementados

### 6.1 `trg_verificar_producto_fk`

**Tabla:** `venta_detalle`

**Evento:** `BEFORE INSERT OR UPDATE`

**Función:** `verificar_producto_existente()`

**Propósito:**
- Simula la integridad referencial que no puede establecerse con FK debido a la herencia.
- Verifica que `id_producto` exista en la tabla `producto` (o sus hijos).
- Lanza excepción con código `23503` (foreign_key_violation) si no existe.

**Lógica:**
```sql
IF NOT EXISTS (SELECT 1 FROM producto WHERE id = NEW.id_producto) THEN
    RAISE EXCEPTION 'Violación de integridad referencial: El producto ID % no existe.', NEW.id_producto
    USING ERRCODE = '23503';
END IF;
```

---

### 6.2 `trg_gestion_stock`

**Tabla:** `venta_detalle`

**Evento:** `AFTER INSERT OR UPDATE OR DELETE`

**Función:** `gestionar_stock()`

**Propósito:**
- Gestionar automáticamente el inventario (`producto.cantidad`) cuando se agregan, modifican o eliminan detalles de venta.

**Lógica:**

| Operación | Acción                                                   |
|-----------|----------------------------------------------------------|
| `INSERT`  | Resta `cantidad` del producto. Verifica stock suficiente.|
| `DELETE`  | Devuelve `cantidad` al producto.                         |
| `UPDATE`  | Ajusta la diferencia: `cantidad - (NEW.cantidad - OLD.cantidad)` |

**Validación:**
- Lanza excepción si el stock es insuficiente:
```sql
IF (SELECT cantidad FROM producto WHERE id = NEW.id_producto) < NEW.cantidad THEN
    RAISE EXCEPTION 'Stock insuficiente para el producto ID %', NEW.id_producto;
END IF;
```

---

### 6.3 `trg_calcular_total_venta`

**Tabla:** `venta_detalle`

**Evento:** `AFTER INSERT OR UPDATE OR DELETE`

**Función:** `calcular_total_venta()`

**Propósito:**
- Recalcular automáticamente el `precio_total` en la tabla `venta` cuando se modifican los detalles.

**Lógica:**
1. Identifica el `id_venta` afectado.
2. Suma todos los `cantidad * precio` de esa venta.
3. Actualiza `venta.precio_total` con el nuevo total.

```sql
SELECT COALESCE(SUM(cantidad * precio), 0)
INTO v_nuevo_total
FROM venta_detalle
WHERE id_venta = v_id_venta_afectada;

UPDATE venta SET precio_total = v_nuevo_total WHERE id = v_id_venta_afectada;
```

---

## 7. Funciones SQL

### 7.1 `insertar_venta()`

**Firma:**
```sql
insertar_venta(
    p_detalles VARCHAR(200),
    p_venta_detalle JSONB,
    p_fecha DATE DEFAULT CURRENT_DATE
) RETURNS INTEGER
```

**Propósito:**
- Crear una venta completa (cabecera + detalles) en una sola transacción.
- Retorna el `id` de la venta creada.

**Parámetros:**
- `p_detalles`: Descripción de la venta.
- `p_venta_detalle`: Array JSON con los productos a vender.
- `p_fecha`: Fecha de la venta (opcional, por defecto es la fecha actual).

**Formato del JSON:**
```json
[
    {"id_producto": 9, "cantidad": 10, "precio": 35.00},
    {"id_producto": 12, "cantidad": 6, "precio": 72.00}
]
```

**Flujo de ejecución:**
1. Inserta registro en `venta` con `precio_total = 0`.
2. Itera sobre el array JSON.
3. Inserta cada elemento en `venta_detalle`.
4. Los triggers se encargan de:
   - Validar existencia del producto (`trg_verificar_producto_fk`).
   - Actualizar stock (`trg_gestion_stock`).
   - Calcular total (`trg_calcular_total_venta`).
5. Retorna el `id` de la venta.

**Manejo de errores:**
- Captura cualquier excepción y lanza mensaje personalizado.

---

## 8. Consideraciones para el ORM

### 8.1 Mapeo de Herencia en SQLAlchemy

**Opciones disponibles:**

1. **Joined Table Inheritance** (más cercano a la implementación PostgreSQL):
   - Cada tabla hija es una tabla separada.
   - Se realiza JOIN automático para obtener datos completos.
   - **Recomendado** para esta estructura.

2. **Concrete Table Inheritance**:
   - Cada tabla hija contiene todos los campos (duplicación).
   - No refleja exactamente la herencia nativa de PostgreSQL.

### 8.2 Tipos Compuestos

- `price_size` y `price_amount` deben mapearse usando `sqlalchemy.dialects.postgresql.CompositeType`.
- Alternativamente, usar columnas JSON/JSONB si el ORM no soporta bien composite types.

### 8.3 Arrays PostgreSQL

- `ingredientes` es de tipo `TEXT[]`.
- En SQLAlchemy: `ARRAY(Text)` de `sqlalchemy.dialects.postgresql`.

### 8.4 ENUM Types

- Usar `sqlalchemy.Enum` con valores específicos de cada tipo.
- O mapear como `VARCHAR` y validar en Pydantic.

### 8.5 Relación `venta_detalle` → `producto`

- **Problema:** No hay FK explícita por la herencia.
- **Solución:** En el ORM, usar `relationship` sin `foreign_keys` o definir `remote_side` manualmente.

---

## 9. Restricciones y Validaciones

| Elemento              | Restricción/Validación                                       |
|-----------------------|--------------------------------------------------------------|
| `producto.id`         | SERIAL PRIMARY KEY (auto-incremental)                        |
| `venta_detalle.id_producto` | Validado mediante trigger (no FK explícita)            |
| Stock                 | Trigger valida que `cantidad >= cantidad_vendida`            |
| `precio_total`        | Calculado automáticamente (trigger)                          |
| `venta.fecha`         | DEFAULT CURRENT_DATE                                         |
| Tipos ENUM            | Valores restringidos a los definidos en cada ENUM            |

---

## 10. Valores por Defecto

| Campo         | Valor por Defecto    |
|---------------|----------------------|
| `venta.fecha` | `CURRENT_DATE`       |
| `producto.id` | Auto-incremental     |
| `venta.precio_total` | Calculado por trigger |

---

## 11. Resumen de Comportamiento de los Triggers

**Al insertar en `venta_detalle`:**
1. ✅ Valida existencia del producto.
2. ✅ Verifica stock suficiente.
3. ✅ Resta stock del inventario.
4. ✅ Recalcula `precio_total` de la venta.

**Al actualizar `venta_detalle`:**
1. ✅ Valida existencia del producto.
2. ✅ Ajusta stock (diferencia entre old y new).
3. ✅ Recalcula `precio_total` de la venta.

**Al eliminar de `venta_detalle`:**
1. ✅ Devuelve stock al inventario.
2. ✅ Recalcula `precio_total` de la venta.

**Al eliminar de `venta`:**
1. ✅ Elimina en cascada todos los `venta_detalle`.
2. ✅ Los triggers de `venta_detalle` devuelven el stock.

---

## 12. Conclusiones para la Implementación del Backend

1. **No inventar campos adicionales:** Respetar estrictamente esta estructura.
2. **Herencia:** Implementar usando Joined Table Inheritance en SQLAlchemy.
3. **Tipos compuestos:** Mapear `price_size` y `price_amount` correctamente.
4. **Función SQL:** Crear wrapper Python para `insertar_venta()` usando `text()`.
5. **Triggers:** No reimplementar en Python; dejar que PostgreSQL los maneje.
6. **Validaciones:** Pueden agregarse en Pydantic schemas, pero sin contradecir la DB.
7. **Relaciones:** Manejar cuidadosamente la relación `venta_detalle` → `producto` sin FK explícita.

---

**Fin del análisis. No se ha escrito código aún.**
