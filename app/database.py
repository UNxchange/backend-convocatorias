import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv() # Carga las variables desde el archivo .env

MONGO_URI = os.getenv("MONGO_URI")
DATABASE_NAME = os.getenv("DATABASE_NAME")

# Se crea una única instancia del cliente para ser reutilizada
client = AsyncIOMotorClient(MONGO_URI)
database = client[DATABASE_NAME]

# Función para obtener la colección de convocatorias
def get_convocatoria_collection():
    return database.get_collection("convocatorias")