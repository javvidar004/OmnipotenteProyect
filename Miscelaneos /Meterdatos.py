import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os

load_dotenv()

DB_CONFIG = {
    'host': os.getenv("DB_HOST"),
    'database': os.getenv("DB_NAME"),
    'user': os.getenv("DB_USER"),
    'password': os.getenv("DB_PASSWORD"),
    'port': int(os.getenv("DB_PORT"))
}

def conectar_db():
    try:
        return mysql.connector.connect(**DB_CONFIG)
    except Error as e:
        print(f"Error de conexión: {e}")
        return None
    
conectar_db()