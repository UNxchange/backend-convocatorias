#!/usr/bin/env python3
"""
Script para probar todos los endpoints del backend de convocatorias
"""
import requests
import json
import time

BASE_URL = "http://localhost:8008"

def test_endpoints():
    print("🧪 PROBANDO ENDPOINTS DEL BACKEND")
    print("=" * 50)
    
    # Test 1: Endpoint raíz
    print("\n1️⃣ Probando endpoint raíz...")
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 2: Listar todas las convocatorias
    print("\n2️⃣ Probando GET /convocatorias...")
    try:
        response = requests.get(f"{BASE_URL}/convocatorias")
        print(f"   Status: {response.status_code}")
        data = response.json()
        print(f"   Total convocatorias: {len(data)}")
        if data:
            print(f"   Primera convocatoria: {data[0]['institution']} - {data[0]['country']}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 3: Búsqueda por país
    print("\n3️⃣ Probando filtro por país (Alemania)...")
    try:
        response = requests.get(f"{BASE_URL}/convocatorias?country=Alemania")
        print(f"   Status: {response.status_code}")
        data = response.json()
        print(f"   Convocatorias en Alemania: {len(data)}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 4: Búsqueda por idioma
    print("\n4️⃣ Probando filtro por idioma (inglés)...")
    try:
        response = requests.get(f"{BASE_URL}/convocatorias?language=inglés")
        print(f"   Status: {response.status_code}")
        data = response.json()
        print(f"   Convocatorias en inglés: {len(data)}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 5: Búsqueda por estado
    print("\n5️⃣ Probando filtro por estado (Vigente)...")
    try:
        response = requests.get(f"{BASE_URL}/convocatorias?state=Vigente")
        print(f"   Status: {response.status_code}")
        data = response.json()
        print(f"   Convocatorias vigentes: {len(data)}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 6: Búsqueda de texto libre
    print("\n6️⃣ Probando búsqueda de texto libre (Universidad)...")
    try:
        response = requests.get(f"{BASE_URL}/convocatorias?q=Universidad")
        print(f"   Status: {response.status_code}")
        data = response.json()
        print(f"   Resultados para 'Universidad': {len(data)}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 7: Paginación
    print("\n7️⃣ Probando paginación (limit=5)...")
    try:
        response = requests.get(f"{BASE_URL}/convocatorias?limit=5")
        print(f"   Status: {response.status_code}")
        data = response.json()
        print(f"   Resultados con límite 5: {len(data)}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 8: Obtener convocatoria específica (usando el ID del primer resultado)
    print("\n8️⃣ Probando GET convocatoria específica...")
    try:
        # Primero obtenemos una convocatoria para tener un ID válido
        response = requests.get(f"{BASE_URL}/convocatorias?limit=1")
        if response.status_code == 200 and response.json():
            conv_id = response.json()[0]['id']
            response = requests.get(f"{BASE_URL}/convocatorias/{conv_id}")
            print(f"   Status: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"   Institución: {data['institution']}")
                print(f"   País: {data['country']}")
        else:
            print("   ❌ No se pudo obtener ID de prueba")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print("\n✅ PRUEBAS COMPLETADAS")
    print("🌐 Puedes ver la documentación en: http://localhost:8008/docs")

if __name__ == "__main__":
    # Esperar un momento para que el servidor esté listo
    print("⏳ Esperando que el servidor esté listo...")
    time.sleep(2)
    test_endpoints()