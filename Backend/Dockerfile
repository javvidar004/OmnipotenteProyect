
# Usa una imagen base con Python
FROM python:3.10
# Define el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia los archivos del backend al contenedor
COPY . .

# Instala las dependencias
RUN pip install --default-timeout=400 --no-cache-dir -r requirements.txt

# Expone el puerto en el que corre FastAPI
EXPOSE 5000

# Comando para ejecutar la app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000","--reload"]
