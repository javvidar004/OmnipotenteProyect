from fastapi.middleware.cors import CORSMiddleware  
import mysql.connector
from dotenv import load_dotenv
import os
from fastapi import FastAPI, Form
from fastapi.responses import JSONResponse
from fastapi.responses import RedirectResponse
from sklearn.linear_model import LogisticRegression
import numpy as np 
from collections import Counter

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_methods=["*"],
    allow_headers=["*"],
)


db = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME"),
    port=int(os.getenv("DB_PORT"))
)

#prueba
@app.get("/")
def read_root():
    return {"message": "Hola desde FastAPI"}

@app.get("/geojson/secciones")
def obtener_geojson():
    conn = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        port=int(os.getenv("DB_PORT"))
    )
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id_seccion, coord_inicio_x, coord_inicio_y, coord_fin_x, coord_fin_y, nombre_calle FROM seccion")

    datos = cursor.fetchall()
    cursor.close()
    conn.close()

    features = []
    for fila in datos: 
        geometry = {
            "type": "LineString",
            "coordinates": [
                [float(fila["coord_inicio_x"]), float(fila["coord_inicio_y"])],
                [float(fila["coord_fin_x"]), float(fila["coord_fin_y"])]
            ]
        }
        properties = {
            "id": fila["id_seccion"],
            "name": fila["nombre_calle"]
        }
        features.append({
            "type": "Feature",
            "geometry": geometry,
            "properties": properties
        })

    geojson = {
        "type": "FeatureCollection",
        "features": features
    }
    return JSONResponse(content=geojson)

@app.post("/reportes")
def guardar_reporte(
    id_seccion: str = Form(...),
    fecha: str = Form(...),
    tipo: str = Form(...),
    reporte: str = Form(...)
):
    cursor = db.cursor()
    query = "INSERT INTO reportes (id_seccion, fecha, tipo, reporte) VALUES (%s, %s, %s, %s)"
    valores = (id_seccion, fecha, tipo, reporte)

    cursor.execute(query, valores)
    db.commit()
    cursor.close()

    #return JSONResponse(content={"mensaje": "Reporte guardado correctamente"})
    return RedirectResponse(url="http://127.0.0.1:3000/Frontend/index.html", status_code=303)


@app.get("/geojson/secciones/especiales")
def obtener_geojson():
    conn = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        port=int(os.getenv("DB_PORT"))
    )
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT sec.id_seccion, sec.coord_inicio_x, sec.coord_inicio_y, sec.coord_fin_x, sec.coord_fin_y, sec.nombre_calle, COUNT(rep.tipo) AS reportes FROM seccion AS sec LEFT JOIN reportes AS rep ON sec.id_seccion = rep.id_seccion AND (rep.tipo = 'Extorsion' or rep.tipo = 'Secuestro' or rep.tipo = 'Asalto'or rep.tipo = 'riña') GROUP BY sec.id_seccion")

    datos = cursor.fetchall()
    cursor.close()
    conn.close()

    features = []
    for fila in datos: 
        geometry = {
            "type": "LineString",
            "coordinates": [
                [float(fila["coord_inicio_x"]), float(fila["coord_inicio_y"])],
                [float(fila["coord_fin_x"]), float(fila["coord_fin_y"])]
            ]
        }
        properties = {
            "id": fila["id_seccion"],
            "name": fila["nombre_calle"],
            "reportes":fila["reportes"]
        }
        features.append({
            "type": "Feature",
            "geometry": geometry,
            "properties": properties
        })

    geojson = {
        "type": "FeatureCollection",
        "features": features
    }
    return JSONResponse(content=geojson)

@app.get("/incidentes")
def obtener_incidentes():
    conn = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        port=int(os.getenv("DB_PORT"))
    )

    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT rep.id_reporte, rep.id_seccion, rep.fecha, rep.tipo, rep.reporte FROM reportes AS rep;")

    datos = cursor.fetchall()
    cursor.close()
    conn.close()

#{'id_reporte': 1, 'id_seccion': 144, 'fecha': datetime.datetime(2025, 5, 21, 11, 11), 'tipo': 'Extorsion', 'reporte': 'Bruno'}

    calles = []
    DatosGenerales = []

    for i in datos:
        properties = {
            "section": i['id_seccion'],
            "fecha": {
                'yr': i['fecha'].year,
                'mes': i['fecha'].month,
                'dia': i['fecha'].day,
                'hora': i['fecha'].hour,
                'minuto': i['fecha'].minute
            }
        }
        calles.append(i['id_seccion'])
        DatosGenerales.append(properties)

    CantCalles = Counter(calles)
    calles = list(set(calles))
    ReportesXCalle = []
    for i in calles:
        Calle = {
            "calle": i,
            "horas": [x["fecha"]["hora"] for x in DatosGenerales if x["section"] == i],
            "reportes": CantCalles[i]
        }
        ReportesXCalle.append(Calle)

    return JSONResponse(ReportesXCalle)

