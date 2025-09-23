#!/usr/bin/env python3
"""
Script para probar la conexión a MongoDB local
"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

async def test_mongodb_connection():
    """Prueba la conexión a MongoDB local"""
    load_dotenv()
    
    MONGO_URI = os.getenv("MONGO_URI")
    DATABASE_NAME = os.getenv("DATABASE_NAME")
    
    print(f"🔗 Intentando conectar a: {MONGO_URI}")
    print(f"📋 Base de datos: {DATABASE_NAME}")
    
    try:
        # Crear cliente y conectar
        client = AsyncIOMotorClient(MONGO_URI)
        
        # Probar la conexión
        await client.admin.command('ping')
        print("✅ ¡Conexión exitosa a MongoDB!")
        
        # Obtener información del servidor
        server_info = await client.admin.command('serverStatus')
        print(f"📊 Versión de MongoDB: {server_info['version']}")
        print(f"🏠 Host: {server_info['host']}")
        
        # Acceder a la base de datos
        database = client[DATABASE_NAME]
        
        # Listar colecciones existentes
        collections = await database.list_collection_names()
        print(f"📚 Colecciones existentes: {collections}")
        
        # Probar creación de colección
        collection = database.get_collection("convocatorias")
        count = await collection.count_documents({})
        print(f"📄 Documentos en 'convocatorias': {count}")
        
        # Cerrar conexión
        client.close()
        print("🔒 Conexión cerrada correctamente")
        
        return True
        
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return False

if __name__ == "__main__":
    asyncio.run(test_mongodb_connection())