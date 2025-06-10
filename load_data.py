import json
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os
from app.models import ConvocatoriaCreate  # Importamos el modelo para validar

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DATABASE_NAME = os.getenv("DATABASE_NAME")

async def load_data():
    client = AsyncIOMotorClient(MONGO_URI)
    db = client[DATABASE_NAME]
    collection = db.get_collection("convocatorias")

    # Opcional: Limpiar la colección antes de insertar nuevos datos
    await collection.delete_many({})
    print("Colección 'convocatorias' limpiada.")

    # Cargar los datos desde el archivo JSON pre-procesado
    with open('DataConvenios_limpio.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    convocatorias_to_insert = []
    for item in data:
        try:
            # Validar cada item con Pydantic antes de agregarlo
            convocatoria_model = ConvocatoriaCreate(**item)
            convocatorias_to_insert.append(convocatoria_model.dict(by_alias=True))
        except Exception as e:
            print(f"Error de validación en el item: {item}. Error: {e}")

    if convocatorias_to_insert:
        result = await collection.insert_many(convocatorias_to_insert)
        print(f"Se insertaron {len(result.inserted_ids)} documentos en la base de datos.")
    else:
        print("No se encontraron documentos válidos para insertar.")

    # Crear el índice de texto si no existe
    await collection.create_index([
        ("institution", "text"),
        ("country", "text"),
        ("properties", "text")
    ], name="search_index")
    print("Índice de texto asegurado.")

    client.close()

if __name__ == "__main__":
    asyncio.run(load_data())