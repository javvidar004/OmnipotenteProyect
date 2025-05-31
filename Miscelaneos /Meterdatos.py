#Dependencias 
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os
import json 

load_dotenv()

#conexion
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

def insertar_seccion(coord_inicio_x, coord_inicio_y, coord_fin_x, coord_fin_y, cod_pstl, nombre_calle):
    conexion = conectar_db()
    try:
        # Verificar los valores que estás pasando
        #print(f"Intentando insertar sección: {nombre_calle}")
        #print(f"Coord Inicio: ({coord_inicio_x}, {coord_inicio_y})")
        #print(f"Coord Fin: ({coord_fin_x}, {coord_fin_y})")
        #print(f"Codigo Postal: {cod_pstl}")
        #print(f"Nombre Calle: {nombre_calle}")
        
        # Verificar que las coordenadas no sean listas
        if isinstance(coord_inicio_x, list) or isinstance(coord_inicio_y, list):
            raise ValueError("Las coordenadas de inicio no deben ser listas.")
        if isinstance(coord_fin_x, list) or isinstance(coord_fin_y, list):
            raise ValueError("Las coordenadas de fin no deben ser listas.")
        
        # Asegúrate de que el código postal no sea una lista o algún otro tipo incorrecto
        if isinstance(cod_pstl, list):
            raise ValueError("El código postal no debe ser una lista.")
        
        # Si el nombre de la calle es una lista, convertirlo a cadena
        if isinstance(nombre_calle, list):
            print("El nombre de la calle es una lista, convirtiendo a cadena...")
            nombre_calle = ', '.join(nombre_calle)
        
        cursor = conexion.cursor()
        cursor.execute("""
            INSERT INTO seccion
            (coord_inicio_x, coord_inicio_y, coord_fin_x, coord_fin_y, cod_pstl, nombre_calle)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (coord_inicio_x, coord_inicio_y, coord_fin_x, coord_fin_y, cod_pstl, nombre_calle))
        conexion.commit()
        print(f"✅ Sección insertada: {nombre_calle}")
    except Exception as e:
        print(f"❌ Error al insertar sección: {e}")


def Crear_secciones(cp):
    with open("/home/vboxuser/Documents/ProyectoIA/OmnipotenteProyect/Miscelaneos /"+cp+".geojson", "r", encoding="utf-8") as archivo:datos = json.load(archivo)


    for feature in datos["features"]:
        nombre_calle = feature["properties"].get("name", "SIN_NOMBRE")
        codigo = cp
        coords = feature["geometry"]["coordinates"]

        # Asegura que sea LineString y que los coords sean una lista de pares [x, y]
        if feature["geometry"]["type"] == "LineString":
            xi, yi = coords[0]
            for x, y in coords[1:]:
                insertar_seccion(xi, yi, x, y, codigo, nombre_calle)
                xi, yi = x, y
        else:
            print(f"⚠️ Tipo de geometría no soportado: {feature['geometry']['type']}")

colonias_benito_juarez = [
    ("8 de Agosto", "03820"),
    ("Acacias", "03240"),
    ("Actipan", "03230"),
    ("Álamos", "03400"),
    ("Albert", "03560"),
    ("Américas Unidas", "03610"),
    ("Ampliación Nápoles", "03840"),
    ("Atenor Salas", "03010"),
    ("Ciudad de los Deportes", "03710"),
    ("Crédito Constructor", "03940"),
    ("Del Carmen", "03540"),
    ("Del Lago", "03640"),
    ("Del Valle Centro", "03100"),
    ("Del Valle Norte", "03103"),
    ("Del Valle Sur", "03104"),
    ("Ermita", "03590"),
    ("Extremadura Insurgentes", "03740"),
    ("General Pedro María Anaya", "03340"),
    ("Independencia", "03630"),
    ("Insurgentes Mixcoac", "03920"),
    ("Insurgentes San Borja", "03100"),
    ("Iztaccihuatl", "03520"),
    ("Josefa Ortiz de Domínguez", "03430"),
    ("Letrán Valle", "03650"),
    ("Merced Gómez", "03930"),
    ("Miguel Alemán", "03420"),
    ("Miravalle", "03580"),
    ("Mixcoac", "03910"),
    ("Moderna", "03510"),
    ("Nápoles", "03810"),
    ("Narvarte Oriente", "03023"),
    ("Narvarte Poniente", "03020"),
    ("Nativitas", "03500"),
    ("Niños Héroes", "03440"),
    ("Nochebuena", "03720"),
    ("Periodista", "03620"),
    ("Piedad Narvarte", "03000"),
    ("Portales Norte", "03303"),
    ("Portales Oriente", "03570"),
    ("Portales Sur", "03300"),
    ("Postal", "03410"),
    ("Residencial Emperadores", "03320"),
    ("San José Insurgentes", "03900"),
    ("San Juan", "03730"),
    ("San Pedro de los Pinos", "03800"),
    ("San Simón Ticumac", "03660"),
    ("Santa Cruz Atoyac", "03310"),
    ("Santa María Nonoalco", "03700"),
    ("Tlacoquemécatl", "03200"),
    ("Vértiz Narvarte", "03600"),
    ("Villa de Cortés", "03530"),
    ("Xoco", "03330"),
    ("Zacahuitzco", "03550"),
]

for Col,Cod in colonias_benito_juarez:
    insertar_zona(Cod, "CDMX", "Benito Juárez", "16260 ", "-1.550")

Crear_secciones("03920")
Crear_secciones("03910")

col = ["03910","03700","03740","03730","03720","03200","03900","03104","03230"]
for n in col:
    Crear_secciones(n)
