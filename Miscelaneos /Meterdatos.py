import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os
import json 

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

def obtener_zonas():
    conexion = conectar_db()
    if conexion:
        try:
            cursor = conexion.cursor(dictionary=True)
            cursor.execute("SELECT * FROM zonas")
            zonas = cursor.fetchall()
            for zona in zonas:
                print(zona)
            return zonas
        except Error as e:
            print(f"Error al consultar zonas: {e}")
        finally:
            cursor.close()
            conexion.close()
    else:
        print("No se pudo conectar a la base de datos.")

def insertar_zona(cod_pstl, estado, colonia, densidad, marginacion):
    conexion = conectar_db()
    if conexion:
        try:
            cursor = conexion.cursor()
            cursor.execute("""INSERT INTO zonas (cod_pstl, estado, colonia, densidad_poblacion, indice_marginacion) VALUES (%s, %s, %s, %s, %s)""", 
            (cod_pstl, estado, colonia, densidad, marginacion))
            conexion.commit()
            print("Zona insertada correctamente ✅")
        except Error as e:
            print(f"Error al insertar zona: {e}")
        finally:
            cursor.close()
            conexion.close()

def insertar_seccion( coord_inicio_x, coord_inicio_y, coord_fin_x, coord_fin_y, cod_pstl, nombre_calle):
    conexion = conectar_db()
    if conexion:
        try:
            cursor = conexion.cursor()
            cursor.execute("""
                INSERT INTO seccion 
                (coord_inicio_x, coord_inicio_y, coord_fin_x, coord_fin_y, cod_pstl, nombre_calle) 
                VALUES ( %s, %s, %s, %s, %s, %s)
            """, ( coord_inicio_x, coord_inicio_y, coord_fin_x, coord_fin_y, cod_pstl, nombre_calle))
            conexion.commit()
            print("Sección insertada correctamente ✅")
        except Error as e:
            print(f"Error al insertar sección: {e}")
        finally:
            cursor.close()
            conexion.close()


with open("/home/vi3rn35/Documents/Escuela/3er semestre/BDD/Charly_proyecto/Miscelaneos /casa_segmentos.geojson", "r", encoding="utf-8") as archivo:
    datos = json.load(archivo)

insertar_zona(14230, "CDMX", "Tlalpan", "1530", "-1.738")


for feature in datos["features"]:

    nombre_calle = feature["properties"]["name"]
    codigo = 14230
    xi,yi = 0,0
    bnd = 0

    for x,y in (feature["geometry"]["coordinates"]):
        if bnd != 0:
            insertar_seccion( xi, yi, x, y, codigo, nombre_calle)
            xi,yi = x,y
        else:
            xi,yi = x,y
            bnd = 1








