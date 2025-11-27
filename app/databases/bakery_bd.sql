-- ============================================
-- TIPOS DE DATOS
-- ============================================

-- TIPO DE DATO PRECIO SEGUN TAMAÑO
CREATE TYPE price_size AS (
	small NUMERIC(10,2),
	medium NUMERIC(10,2),
	big NUMERIC(10,2)
);

-- TIPO DE DATO ESTATUS SEGUN TAMAÑO (TRUE = HAY, FALSE = NO HAY)
CREATE TYPE status_size AS (
    small BOOLEAN,
    medium BOOLEAN,
    big BOOLEAN
);

-- TIPO DE DATO PRECIO SEGUN CANTIDAD
CREATE TYPE price_amount AS (
	retail_sale NUMERIC(10,2), --AL POR MENOR
	wholesale NUMERIC(10,2) --AL POR MAYOR
);

-- TIPO DE DATO: TIPOS DE POSTRES
CREATE TYPE type_dessert AS ENUM(
	'Pastel',
	'Tarta',
	'Helado',
	'Pudín',
	'Flan',
	'Gelatina',
	'Galleta',
	'Mousses',
	'Crepa'
);

-- TIPO DE DATO: TIPOS DE PAN
CREATE TYPE type_bread AS ENUM(
	'Dulce',
	'Salado'
);

-- TIPO DE DATO: TIPOS DE BEBIDA
CREATE TYPE type_drink AS ENUM(
	'Batido',
	'Smoothie',
	'Frappé',
	'Licuado',
	'Malteada',
	'Café'
);

-- TIPO DE DATO: TIPO DE EXTRA
CREATE TYPE type_extra AS ENUM(
	'Vela',
	'Molde',
	'Plato',
	'Vaso',
	'Charola'
);

-- TIPO DE DATO PARA MANEJAR VARIANTES
CREATE TYPE type_variant AS ENUM ('small', 'medium', 'big', 'retail', 'wholesale');

-- ============================================
-- TABLAS
-- ============================================

-- TABLA PADRE: PRODUCTO
CREATE TABLE producto (
	id SERIAL PRIMARY KEY,
	nombre VARCHAR(50) NOT NULL,
	descripcion TEXT,
	imagen_url TEXT NOT NULL
);

-- TABLA HIJO DE PRODUCTO: POSTRE
CREATE TABLE postre (
	tipo_postre type_dessert,
	precio price_size, --PRECIO SEGUN TAMAÑO
	disponible status_size, -- DISPONIBLE SEGUN TAMAÑO
	ingredientes TEXT[] NOT NULL,
	es_dulce BOOLEAN NOT NULL
) INHERITS (producto);

-- TABLA HIJO DE PRODUCTO: PAN
CREATE TABLE pan (
	tipo_pan type_bread,
	precio price_amount, --PRECIO SEGUN CANTIDAD
	disponible BOOLEAN DEFAULT TRUE,
	ingredientes TEXT[] NOT NULL
) INHERITS (producto);

-- TABLA HIJO DE PRODUCTO: BEBIDA
CREATE TABLE bebida (
	tipo_bebida type_drink,
	precio price_size, --PRECIO SEGUN TAMAÑO
	disponible status_size, -- DISPONIBLE SEGUN TAMAÑO
	ingredientes TEXT[] NOT NULL,
	es_fria BOOLEAN DEFAULT TRUE
) INHERITS (producto);

-- TABLA HIJO DE PRODUCTO: EXTRA
CREATE TABLE extra (
	tipo_extra type_extra,
	precio price_amount, --PRECIO SEGUN CANTIDAD
	disponible BOOLEAN DEFAULT TRUE
) INHERITS (producto);

-- TABLA: VENTA
CREATE TABLE venta (
	id SERIAL PRIMARY KEY,
	detalles VARCHAR(200),
	fecha DATE DEFAULT CURRENT_DATE,
	precio_total NUMERIC(10,2)
);

-- TABLA: VENTA DETALLE
CREATE TABLE venta_detalle (
	id SERIAL PRIMARY KEY,
	id_venta INTEGER,
	id_producto INTEGER NOT NULL, -- NO HAY REFERENCIA DIRECTA A LA TABLA PRODUCTO
	cantidad INTEGER NOT NULL,
	precio NUMERIC(10,2),
	variante type_variant,
	FOREIGN KEY (id_venta) REFERENCES venta(id) ON DELETE CASCADE
);


-- ============================================
-- TRIGGER PARA VERIFICAR QUE EL PRODUCTO EXISTA
-- (SIMULA LA INTEGRIDAD REFERENCIAL EN VENTA_DETALLE)
-- ============================================
CREATE OR REPLACE FUNCTION verificar_producto_existente()
RETURNS TRIGGER AS 
$BODY$
BEGIN
	IF NOT EXISTS (SELECT 1 FROM producto WHERE id = NEW.id_producto) THEN
		RAISE EXCEPTION 'Violación de integridad referencial: El producto ID % no existe.', NEW.id_producto
		USING ERRCODE = '23503'; -- Código estándar de foreign_key_violation
	END IF;

	RETURN NEW;
END;
$BODY$
LANGUAGE 'plpgsql';

CREATE TRIGGER trg_verificar_producto_fk
BEFORE INSERT OR UPDATE 
ON venta_detalle
FOR EACH ROW
EXECUTE PROCEDURE verificar_producto_existente();


-- ============================================
-- TRIGGER PARA ACTUALIZAR EL INVENTARIO
-- ============================================
CREATE OR REPLACE FUNCTION verificar_disponibilidad()
RETURNS TRIGGER AS
$BODY$
DECLARE
	r_postre postre%ROWTYPE;
	r_bebida bebida%ROWTYPE;
	r_pan pan%ROWTYPE;
	r_extra extra%ROWTYPE;
BEGIN
	IF (TG_OP = 'INSERT' OR TG_OP = 'UPDATE') THEN
		-- VERIFICAR SI ES POSTRE
		SELECT * INTO r_postre FROM postre WHERE id = NEW.id_producto;
		IF FOUND THEN
			IF NEW.variante = 'small' AND NOT (r_postre.disponible).small THEN
				RAISE EXCEPTION 'Lo sentimos, el tamaño PEQUEÑO de % está agotado.', r_postre.nombre;
			ELSIF NEW.variante = 'medium' AND NOT (r_postre.disponible).medium THEN
				RAISE EXCEPTION 'Lo sentimos, el tamaño MEDIANO de % está agotado.', r_postre.nombre;
			ELSIF NEW.variante = 'big' AND NOT (r_postre.disponible).big THEN
				RAISE EXCEPTION 'Lo sentimos, el tamaño GRANDE de % está agotado.', r_postre.nombre;
			END IF;
			RETURN NEW;
		END IF;

		-- VERIFICAR SI ES BEBIDA
		SELECT * INTO r_bebida FROM bebida WHERE id = NEW.id_producto;
		IF FOUND THEN
			IF NEW.variante = 'small' AND NOT (r_bebida.disponible).small THEN
				RAISE EXCEPTION 'Lo sentimos, el tamaño PEQUEÑO de % está agotado.', r_bebida.nombre;
			ELSIF NEW.variante = 'medium' AND NOT (r_bebida.disponible).medium THEN
				RAISE EXCEPTION 'Lo sentimos, el tamaño MEDIANO de % está agotado.', r_bebida.nombre;
			ELSIF NEW.variante = 'big' AND NOT (r_bebida.disponible).big THEN
				RAISE EXCEPTION 'Lo sentimos, el tamaño GRANDE de % está agotado.', r_bebida.nombre;
			END IF;
			RETURN NEW;
		END IF;

		-- VERIFICAR SI ES PAN
		SELECT * INTO r_pan FROM pan WHERE id = NEW.id_producto;
		IF FOUND THEN
			IF NOT r_pan.disponible THEN
				RAISE EXCEPTION 'El pan % ya no esta disponible hoy.', r_pan.nombre;
			END IF;
			RETURN NEW;
		END IF;

		-- VERIFICAR SI ES EXTRA
		SELECT * INTO r_extra FROM extra WHERE id = NEW.id_producto;
		IF FOUND THEN
			IF NOT r_extra.disponible THEN
				RAISE EXCEPTION 'El extra % ya no esta disponible.', r_extra.nombre;
			END IF;
			RETURN NEW;
		END IF;
	END IF;
	RETURN NEW;
END;
$BODY$ 
LANGUAGE 'plpgsql';

CREATE TRIGGER trg_gestion_disponibilidad
BEFORE INSERT OR UPDATE
ON venta_detalle
FOR EACH ROW
EXECUTE PROCEDURE verificar_disponibilidad();


-- ============================================
-- TRIGGER PARA CALCULAR EL TOTAL DE LA VENTA
-- ============================================
CREATE OR REPLACE FUNCTION calcular_total_venta()
RETURNS TRIGGER AS
$BODY$
DECLARE
	v_id_venta_afectada INTEGER;
	v_nuevo_total NUMERIC(10,2);
BEGIN
	-- Obtener el ID de la venta afectada
	IF (TG_OP = 'DELETE') THEN
		v_id_venta_afectada := OLD.id_venta;
	ELSE
		v_id_venta_afectada := NEW.id_venta;
	END IF;

	-- Recalcular el total de esa venta especifica
	SELECT COALESCE(SUM(cantidad * precio), 0)
	INTO v_nuevo_total
	FROM venta_detalle
	WHERE id_venta = v_id_venta_afectada;

	-- Actualizar la cabecera
	UPDATE venta
	SET precio_total = v_nuevo_total
	WHERE id = v_id_venta_afectada;

	IF (TG_OP = 'DELETE') THEN
		RETURN OLD;
	ELSE
		RETURN NEW;
	END IF;
END;
$BODY$
LANGUAGE 'plpgsql';

CREATE TRIGGER trg_calcular_total_venta
AFTER INSERT OR UPDATE OR DELETE
ON venta_detalle
FOR EACH ROW
EXECUTE PROCEDURE calcular_total_venta();


-- ============================================
-- FUNCIÓN PARA INSERTAR VENTA CON DETALLES
-- ============================================
CREATE OR REPLACE FUNCTION insertar_venta(
    p_detalles VARCHAR(200),
    p_venta_detalle JSONB,
    p_fecha DATE DEFAULT CURRENT_DATE
) RETURNS INTEGER AS 
$BODY$
DECLARE
	v_id_venta INTEGER;
	v_item JSONB;
BEGIN
	-- Insertar la venta principal (sin precio_total) retornando el id de la venta
	INSERT INTO venta (detalles, fecha, precio_total)
	VALUES (p_detalles, p_fecha, 0)
	RETURNING id INTO v_id_venta;

	-- Iterar sobre los detalles del JSON e insertar cada uno
	FOR v_item IN SELECT jsonb_array_elements(p_venta_detalle)
	LOOP
		INSERT INTO venta_detalle (id_venta, id_producto, cantidad, precio, variante)
		VALUES (
			v_id_venta,
			(v_item->>'id_producto')::INTEGER,
			(v_item->>'cantidad')::INTEGER,
			(v_item->>'precio')::NUMERIC(10,2),
			(v_item->>'variante')::type_variant
		);
	END LOOP;

	-- Retornar el id de la venta creada
	RETURN v_id_venta;

EXCEPTION WHEN OTHERS THEN
	RAISE EXCEPTION 'Error al insertar venta: %', SQLERRM;
END;
$BODY$
LANGUAGE 'plpgsql';


-- ============================================
-- INSERCION DE DATOS EN LOS HIJOS DE LA TABLA PRODUCTO
-- ============================================
INSERT INTO postre(nombre, descripcion, disponible, tipo_postre, precio, ingredientes, es_dulce, imagen_url)
VALUES 
('Pastel de Tres Leches', 'Clásico pastel humedecido en tres leches', ROW(TRUE, FALSE, TRUE), 'Pastel', ROW(250.00, 380.00, 500.00), ARRAY['Leche', 'Leche condensada', 'Harina', 'Huevo', 'Vainilla', 'Canela'], TRUE, 'https://i.pinimg.com/1200x/bb/75/cb/bb75cba80fa655c3a10fe35853dfd7d2.jpg'),  
('Cheesecake de Fresa', 'Pastel de queso con cubierta de mermelada', ROW(TRUE, TRUE, TRUE), 'Pastel', ROW(280.00, 400.00, 550.00), ARRAY['Queso Crema', 'Huevo', 'Galleta', 'Fresa', 'Azúcar'], TRUE, 'https://i.pinimg.com/1200x/02/a4/86/02a486ab4d2db9909d1bbb26d8679b82.jpg'),
('Tarta de Manzana', 'Tarta crujiente con relleno de canela y manzana', ROW(TRUE, TRUE, TRUE), 'Tarta', ROW(120.00, 180.00, 240.00), ARRAY['Manzana', 'Canela', 'Mantequilla', 'Harina'], TRUE, 'https://i.pinimg.com/736x/7e/1d/a8/7e1da82a932ab3c654c81c137158ddd0.jpg'),
('Gelatina Mosaico', 'Gelatina de leche con cubos de sabores', ROW(TRUE, TRUE, TRUE), 'Gelatina', ROW(80.00, 150.00, 200.00), ARRAY['Leche condensada', 'Grenetina', 'Saborizantes'], TRUE, 'https://i.pinimg.com/736x/92/07/91/92079168a9a511cb8a292d8b1edd556b.jpg'),
('Flan Napolitano', 'Flan cremoso con caramelo', ROW(TRUE, TRUE, TRUE), 'Flan', ROW(90.00, 160.00, 220.00), ARRAY['Huevo', 'Leche', 'Caramelo', 'Vainilla'], TRUE, 'https://i.pinimg.com/736x/58/ba/27/58ba27362b2218fb1df0c3fc882276fa.jpg'),
('Mousse de Maracuyá', 'Postre ligero y acidito', ROW(TRUE, TRUE, TRUE), 'Mousses', ROW(45.00, 80.00, 110.00), ARRAY['Maracuyá', 'Crema batida', 'Azúcar'], TRUE, 'https://i.pinimg.com/736x/8a/aa/07/8aaa0760812ee6fbe7f22967e1511cd2.jpg'),
('Crepa Nutella', 'Crepa rellena de avellana', ROW(TRUE, TRUE, TRUE), 'Crepa', ROW(60.00, 85.00, 95.00), ARRAY['Harina', 'Huevo', 'Leche', 'Nutella'], TRUE, 'https://i.pinimg.com/1200x/1b/98/0e/1b980e1f06856c3708d7609268192157.jpg'),
('Crepa de Jamón y Queso', 'Crepa rellena de jamón y queso cheddar', ROW(TRUE, TRUE, TRUE), 'Crepa', ROW(60.00, 85.00, 95.00), ARRAY['Harina', 'Huevo', 'Mantequilla', 'Sal', 'Jamón', 'Queso Cheddar', 'Orégano'], FALSE, 'https://i.pinimg.com/1200x/b1/12/71/b11271156ce0014527b437a57bdb4cdc.jpg');

INSERT INTO pan (nombre, descripcion, disponible, tipo_pan, precio, ingredientes, imagen_url)
VALUES 
('Bolillo Tradicional', 'Pan blanco crujiente por fuera', TRUE, 'Salado', ROW(5.00, 3.50), ARRAY['Harina', 'Levadura', 'Sal', 'Agua'], 'https://i.pinimg.com/736x/2e/95/c6/2e95c6b3872609c21f4d04c424bf77e8.jpg'),
('Baguette Rústica', 'Barra de pan estilo francés', TRUE, 'Salado', ROW(25.00, 18.00), ARRAY['Masa madre', 'Harina', 'Sal'], 'https://i.pinimg.com/1200x/a3/7d/be/a37dbe7b093dacc7f4f05d003cd09294.jpg'),
('Focaccia', 'Pan plano con hierbas finas', TRUE, 'Salado', ROW(35.00, 28.00), ARRAY['Aceite de oliva', 'Romero', 'Harina'], 'https://i.pinimg.com/736x/de/46/67/de4667a733fc82893d6276f75d825207.jpg'),
('Concha de Vainilla', 'Pan dulce con cubierta de azúcar', TRUE, 'Dulce', ROW(12.00, 9.50), ARRAY['Harina', 'Azúcar', 'Mantequilla', 'Huevo', 'Vainilla'], 'https://i.pinimg.com/1200x/b6/52/4f/b6524fdc83aed788d2c89bc89e4d6534.jpg'),
('Dona de Chocolate', 'Dona frita cubierta de chocolate', TRUE, 'Dulce', ROW(15.00, 11.00), ARRAY['Harina', 'Chocolate', 'Huevo', 'Aceite'], 'https://i.pinimg.com/736x/55/f1/c1/55f1c1db9a37a27e3e40eef9cd51cfa0.jpg'),
('Croissant', 'Pan de hojaldre con mantequilla relleno de nutella', TRUE, 'Dulce', ROW(18.00, 14.00), ARRAY['Mantequilla', 'Harina', 'Huevo', 'Levadura', 'Nutella'], 'https://i.pinimg.com/1200x/34/a0/59/34a059a12664dcae118986a011cd897c.jpg');

INSERT INTO bebida (nombre, descripcion, disponible, tipo_bebida, precio, ingredientes, es_fria, imagen_url)
VALUES 
('Licuado de Fresa', 'Licuado con leche entera', ROW(TRUE, TRUE, TRUE), 'Licuado', ROW(35.00, 45.00, 55.00), ARRAY['Leche', 'Fresa', 'Azúcar'], TRUE, 'https://i.pinimg.com/736x/f9/3c/6b/f93c6b3155e9bbf131e20a540881a562.jpg'),
('Frappé Moka', 'Café frío con chocolate', ROW(TRUE, TRUE, TRUE), 'Frappé', ROW(50.00, 65.00, 80.00), ARRAY['Hielo', 'Café', 'Jarabe de chocolate', 'Leche'], TRUE, 'https://i.pinimg.com/1200x/87/3a/dc/873adcbdfa12f06ef0563c389ef72486.jpg'),
('Smoothie Verde', 'Bebida saludable de espinaca y piña', ROW(TRUE, TRUE, TRUE), 'Smoothie', ROW(45.00, 60.00, 70.00), ARRAY['Espinaca', 'Piña', 'Jugo de Naranja'], TRUE, 'https://i.pinimg.com/736x/74/57/0d/74570df7fa8a3025aab55fcf9bf93fbc.jpg'),
('Malteada Vainilla', 'Malteada espesa con helado', ROW(TRUE, TRUE, TRUE), 'Malteada', ROW(60.00, 80.00, 95.00), ARRAY['Helado de vainilla', 'Leche', 'Crema batida'], TRUE, 'https://i.pinimg.com/736x/53/d4/95/53d495255477867fac45cf9ed81804e4.jpg'),
('Batido de Proteína', 'Batido post-entrenamiento sabor chocolate', ROW(TRUE, TRUE, TRUE), 'Batido', ROW(55.00, 70.00, 85.00), ARRAY['Proteína Whey', 'Agua', 'Plátano', 'Avena'], TRUE, 'https://i.pinimg.com/736x/dd/05/51/dd055187dd43ed8f7d388d996168f662.jpg'),
('Café Americano', 'Espresso diluido con agua caliente', ROW(TRUE, TRUE, TRUE), 'Café', ROW(45.00, 55.00, 70.00), ARRAY['Café', 'Agua'], FALSE, 'https://i.pinimg.com/1200x/d6/f2/e9/d6f2e9113aa8f9aef8b59a8e28bd7255.jpg');

INSERT INTO extra (nombre, descripcion, disponible, tipo_extra, precio, imagen_url)
VALUES 
('Vela Mágica', 'Vela de chispas para cumpleaños', TRUE, 'Vela', ROW(15.00, 10.00), 'https://i.pinimg.com/1200x/c7/5c/9b/c75c9b65d8b313b67c5d545e5cb17b69.jpg'),
('Vela Numérica', 'Vela de cera con número', TRUE, 'Vela', ROW(12.00, 8.00), 'https://i.pinimg.com/736x/52/6b/f0/526bf0e368d2d9cc733bbb620086bfe0.jpg'),
('Plato Desechable', 'Paquete de 10 platos pasteleros', TRUE, 'Plato', ROW(25.00, 20.00), 'https://i.pinimg.com/1200x/0f/d7/93/0fd793b072beae091aeca7ecfeb06b59.jpg'),
('Caja de Regalo', 'Caja decorada para transportar pastel', TRUE, 'Charola', ROW(35.00, 28.00), 'https://i.pinimg.com/736x/d0/f2/41/d0f241b6d4b2c3a815d827a0df85f373.jpg'),
('Vaso Cafetero', 'Vaso térmico reutilizable', TRUE, 'Vaso', ROW(80.00, 65.00), 'https://i.pinimg.com/1200x/cf/32/bd/cf32bd01a75f4aecb54745173e332a22.jpg');


CREATE OR REPLACE FUNCTION obtener_ventas_detalles()
RETURNS TABLE (
    id_venta INT,
    fecha DATE,
    productos JSON,
    total NUMERIC(10,2)
) AS
$BODY$
BEGIN
    RETURN QUERY
    SELECT 
        v.id AS id_venta,
        v.fecha,
        json_agg(
            json_build_object(
                'id_producto', vd.id_producto,
                'cantidad', vd.cantidad,
                'precio_unitario', vd.precio,
                'variante', vd.variante
            )
        ) AS productos,
        v.precio_total AS total
    FROM venta v
    LEFT JOIN venta_detalle vd ON v.id = vd.id_venta
    GROUP BY v.id, v.fecha, v.precio_total
    ORDER BY v.fecha DESC;
END;
$BODY$
LANGUAGE 'plpgsql';

SELECT * FROM obtener_ventas_detalles()
-- ============================================
-- LLAMAR A LA FUNCION DE INSERTAR_VENTA:
-- ============================================

SELECT insertar_venta(
	'Venta de crepas',
	'[
	{"id_producto": 7, "cantidad": 1, "precio": 85.00, "variante": "medium"},
	{"id_producto": 8, "cantidad": 1, "precio": 95.00, "variante": "medium"}
	]'::JSONB
) AS id_venta_creada;


-- ERROR
SELECT insertar_venta(
	'Venta de gelatinas',
	'[
	{"id_producto": 26, "cantidad": 3, "precio": 150.00}
	]'::JSONB
) AS id_venta_creada;

SELECT * FROM postre;
SELECT * FROM pan;
SELECT * FROM bebida;
SELECT * FROM extra;
SELECT * FROM producto ORDER BY id;
SELECT * FROM venta;
SELECT * FROM venta_detalle;

