from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware  
import mysql.connector
from dotenv import load_dotenv
import os
from fastapi import FastAPI, Form
from fastapi.responses import JSONResponse
from fastapi.responses import RedirectResponse

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
    return RedirectResponse(url="http://127.0.0.1:3001/Frontend/index.html", status_code=303)


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