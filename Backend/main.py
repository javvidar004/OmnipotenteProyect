from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # Importa CORS
import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

# Configura CORS (¡IMPORTANTE!)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todos los orígenes (en desarrollo)
    allow_methods=["*"],
    allow_headers=["*"],
)

# Conexión a MySQL (tu código existente)
db = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME"),
    port=int(os.getenv("DB_PORT"))
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