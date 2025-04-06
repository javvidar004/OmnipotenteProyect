from fastapi import FastAPI
import mysql.connector
import os

app = FastAPI()

# Conexión a MySQL usando variables de entorno
db = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME"),
    port=os.getenv("DB_PORT")
)

@app.get("/")
def read_root():
    return {"message": "Hola desde FastAPI"}

@app.get("/usuarios")
def get_usuarios():
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM usuarios")
    data = cursor.fetchall()
    cursor.close()
    return data
