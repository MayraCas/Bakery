import psycopg2

class PostreConnection():
    conn = None
    
    def __init__(self):
        try:
            self.conn = psycopg2.connect(
                host="localhost",
                port ="5433",
                database="panaderia",
                user="may_user",
                password="2015"
            )
        except Exception as e:
            print(f"Error connecting to the database: {e}")
            self.conn.close()
    
    def read_all(self):
        with self.conn.cursor() as cursor:
            cursor.execute("SELECT * FROM postre")
            data = cursor.fetchall()
            return data
    
    def write(self, data):
        with self.conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO postre (nombre, descripcion, precio, cantidad, tipo_postre, ingredientes, es_dulce)
                VALUES (%(nombre)s, %(descripcion)s, %(precio)s, %(cantidad)s, %(tipo_postre)s, %(ingredientes)s, %(es_dulce)s)
            """, data)
            self.conn.commit()
    
    
    def __def__(self):
        self.conn.close()