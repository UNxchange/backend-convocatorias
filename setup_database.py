#!/usr/bin/env python3
"""
🚀 Script de Configuración Automática de Base de Datos
Backend de Convocatorias UnxChange

Este script automatiza completamente la configuración de la base de datos desde cero.
"""

import asyncio
import json
import os
import sys
from pathlib import Path

import pymongo
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "unxchange_local")

class DatabaseSetup:
    def __init__(self):
        self.client = None
        self.database = None
        
    async def connect(self):
        """Conectar a MongoDB"""
        try:
            print("🔌 Conectando a MongoDB...")
            self.client = AsyncIOMotorClient(MONGO_URI)
            
            # Verificar conexión
            await self.client.admin.command('ping')
            print(f"✅ Conexión exitosa a MongoDB: {MONGO_URI}")
            
            self.database = self.client[DATABASE_NAME]
            return True
            
        except Exception as e:
            print(f"❌ Error de conexión a MongoDB: {e}")
            print("\n💡 Asegúrate de que:")
            print("   - MongoDB esté instalado y corriendo")
            print("   - El servicio MongoDB esté activo")
            print("   - La URI de conexión sea correcta")
            return False
    
    async def create_database_and_collection(self):
        """Crear base de datos y colección"""
        print(f"📁 Creando base de datos '{DATABASE_NAME}'...")
        
        # Crear colección (se crea automáticamente al insertar el primer documento)
        collection = self.database.get_collection("convocatorias")
        
        # Verificar si ya existe y tiene datos
        count = await collection.count_documents({})
        if count > 0:
            print(f"⚠️  La colección ya existe con {count} documentos")
            response = input("¿Deseas limpiar y repoblar la base de datos? (y/N): ").lower()
            if response == 'y' or response == 'yes':
                await collection.delete_many({})
                print("🧹 Colección limpiada")
            else:
                print("✅ Manteniendo datos existentes")
                return True
        
        return True
    
    async def create_indexes(self):
        """Crear índices optimizados para búsquedas"""
        print("🔍 Creando índices de búsqueda...")
        
        collection = self.database.get_collection("convocatorias")
        
        # Índice de texto completo para búsquedas
        try:
            await collection.create_index([
                ("institution", "text"),
                ("country", "text"),
                ("properties", "text"),
                ("agreementType", "text")
            ], name="search_index")
            print("✅ Índice de texto creado")
        except Exception as e:
            print(f"⚠️  Índice ya existe o error: {e}")
        
        # Índice por país para filtros rápidos
        try:
            await collection.create_index("country", name="country_index")
            print("✅ Índice por país creado")
        except Exception as e:
            print(f"⚠️  Índice por país ya existe o error: {e}")
        
        # Índice por estado (vigente/no vigente)
        try:
            await collection.create_index("state", name="state_index")
            print("✅ Índice por estado creado")
        except Exception as e:
            print(f"⚠️  Índice por estado ya existe o error: {e}")
    
    async def load_data(self):
        """Cargar datos desde el archivo JSON"""
        data_file = Path("DataConvenios_limpio.json")
        
        if not data_file.exists():
            print(f"❌ Archivo de datos no encontrado: {data_file}")
            print("💡 Asegúrate de que 'DataConvenios_limpio.json' esté en el directorio del proyecto")
            return False
        
        print(f"📊 Cargando datos desde {data_file}...")
        
        try:
            with open(data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            collection = self.database.get_collection("convocatorias")
            
            print(f"📝 Insertando {len(data)} convocatorias...")
            result = await collection.insert_many(data)
            
            print(f"✅ {len(result.inserted_ids)} convocatorias insertadas exitosamente")
            return True
            
        except Exception as e:
            print(f"❌ Error cargando datos: {e}")
            return False
    
    async def verify_data(self):
        """Verificar que los datos se cargaron correctamente"""
        print("🔍 Verificando datos cargados...")
        
        collection = self.database.get_collection("convocatorias")
        
        # Contar documentos
        total_count = await collection.count_documents({})
        print(f"📊 Total de convocatorias: {total_count}")
        
        # Verificar algunos países
        countries = await collection.distinct("country")
        print(f"🌍 Países disponibles: {len(countries)}")
        print(f"   Ejemplos: {', '.join(countries[:5])}...")
        
        # Verificar estados
        states = await collection.distinct("state")
        print(f"📋 Estados: {', '.join(states)}")
        
        # Ejemplo de documento
        sample = await collection.find_one()
        if sample:
            print("📄 Ejemplo de documento:")
            print(f"   Institución: {sample.get('institution', 'N/A')}")
            print(f"   País: {sample.get('country', 'N/A')}")
            print(f"   Tipo: {sample.get('agreementType', 'N/A')}")
            print(f"   Estado: {sample.get('state', 'N/A')}")
        
        return total_count > 0
    
    async def close(self):
        """Cerrar conexión"""
        if self.client:
            self.client.close()
            print("🔌 Conexión cerrada")

async def main():
    """Función principal de configuración"""
    print("🚀 Iniciando configuración de base de datos...")
    print("=" * 50)
    
    setup = DatabaseSetup()
    
    try:
        # Paso 1: Conectar
        if not await setup.connect():
            return False
        
        # Paso 2: Crear DB y colección
        if not await setup.create_database_and_collection():
            return False
        
        # Paso 3: Crear índices
        await setup.create_indexes()
        
        # Paso 4: Cargar datos
        if not await setup.load_data():
            return False
        
        # Paso 5: Verificar
        if not await setup.verify_data():
            return False
        
        print("=" * 50)
        print("🎉 ¡Configuración de base de datos completada exitosamente!")
        print(f"📡 MongoDB URI: {MONGO_URI}")
        print(f"💾 Base de datos: {DATABASE_NAME}")
        print("🌐 Backend listo para iniciar en puerto 8008")
        print("\n🚀 Siguiente paso:")
        print("   python start_server.py")
        
        return True
        
    except Exception as e:
        print(f"❌ Error durante la configuración: {e}")
        return False
    
    finally:
        await setup.close()

def check_prerequisites():
    """Verificar prerrequisitos antes de la configuración"""
    print("🔍 Verificando prerrequisitos...")
    
    # Verificar archivo de datos
    if not Path("DataConvenios_limpio.json").exists():
        print("❌ Archivo 'DataConvenios_limpio.json' no encontrado")
        return False
    
    # Verificar módulos requeridos
    try:
        import motor
        import pymongo
        print("✅ Módulos requeridos disponibles")
    except ImportError as e:
        print(f"❌ Módulo faltante: {e}")
        print("💡 Ejecuta: pip install -r requirements.txt")
        return False
    
    # Verificar archivo .env
    if not Path(".env").exists():
        print("⚠️  Archivo .env no encontrado, usando valores por defecto")
        print("💡 Copia .env.example a .env para personalizar configuración")
    else:
        print("✅ Archivo .env encontrado")
    
    return True

if __name__ == "__main__":
    print("🎯 Script de Configuración de Base de Datos")
    print("   Backend de Convocatorias UnxChange")
    print()
    
    # Verificar prerrequisitos
    if not check_prerequisites():
        print("\n❌ Prerrequisitos no cumplidos. Revisa los errores arriba.")
        sys.exit(1)
    
    # Ejecutar configuración
    success = asyncio.run(main())
    
    if success:
        sys.exit(0)
    else:
        print("\n❌ La configuración falló. Revisa los errores arriba.")
        sys.exit(1)