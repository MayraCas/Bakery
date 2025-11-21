from fastapi import FastAPI, HTTPException, Depends
from model.postre_connection import PostreConnection
from schema.postre_schema import PostreSchema

app = FastAPI()
conn = PostreConnection()

@app.get("/")
def root():
    conn
    return "Welcome to the Bakery API!"

@app.get("/postres/get_all")
def get_all_postres():
    items = []
    for data in conn.read_all():
        item = {
            "id": data[0],
            "nombre": data[1],
            "descripcion": data[2],
            "precio": data[3],
            "cantidad": data[4],
            "tipo_postre": data[5],
            "ingredientes": data[6],
            "es_dulce": data[7]
        }
        items.append(item)
    return items


@app.post("/postres/insert")
def insert(postre_data: PostreSchema):
    data = postre_data.dict()
    print(postre_data)
    conn