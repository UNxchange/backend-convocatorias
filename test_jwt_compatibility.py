#!/usr/bin/env python3
"""
Script para probar la validación de tokens JWT con la nueva configuración
"""
import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()

def test_jwt_compatibility():
    """Prueba la compatibilidad de tokens entre backends"""
    print("🧪 PROBANDO COMPATIBILIDAD JWT ENTRE BACKENDS")
    print("=" * 60)
    
    # Configuración actual
    secret_key = os.getenv("SECRET_KEY")
    algorithm = os.getenv("ALGORITHM", "HS256")
    
    print(f"🔑 Secret Key: {secret_key[:20]}..." if secret_key else "❌ SECRET_KEY no encontrada")
    print(f"🛡️ Algorithm: {algorithm}")
    print(f"📍 Backend Convocatorias: http://localhost:8008")
    print(f"📍 Backend Auth: http://localhost:8000")
    
    print(f"\n📝 INSTRUCCIONES:")
    print("1. Obtén un token válido de tu backend de autenticación (puerto 8000)")
    print("2. Pégalo aquí para probar si funciona en el backend de convocatorias")
    print("3. El token debe contener los campos 'sub' (email) y 'role' (administrador/profesional)")
    
    # Solicitar token
    token = input(f"\n🎟️ Pega aquí tu token JWT: ").strip()
    
    if not token:
        print("❌ No se proporcionó token")
        return
    
    print(f"\n🔍 PROBANDO TOKEN EN BACKEND DE CONVOCATORIAS...")
    
    # Headers para la petición
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # Datos de prueba para crear convocatoria
    test_data = {
        "subscriptionYear": "2025",
        "country": "España",
        "institution": "Universidad de Prueba",
        "agreementType": "Intercambio",
        "validity": "Diciembre - 2028",
        "state": "Vigente",
        "subscriptionLevel": "Universidad Nacional de Colombia",
        "languages": ["Español", "Inglés"],
        "dreLink": "http://ejemplo.com/documento.pdf",
        "agreementLink": "http://ejemplo.com/convocatoria",
        "Props": "Prueba de token\nCreación desde script",
        "internationalLink": "http://universidad-ejemplo.es"
    }
    
    try:
        # Intentar crear convocatoria
        response = requests.post(
            "http://localhost:8008/convocatorias",
            headers=headers,
            json=test_data,
            timeout=10
        )
        
        print(f"📊 RESULTADO:")
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 201:
            print("✅ ¡TOKEN VÁLIDO! La convocatoria se creó exitosamente")
            result = response.json()
            print(f"🆔 ID de convocatoria creada: {result.get('id', 'N/A')}")
            print(f"🏫 Institución: {result.get('institution', 'N/A')}")
        elif response.status_code == 401:
            print("❌ TOKEN INVÁLIDO - Error 401 Unauthorized")
            print("🔍 Posibles causas:")
            print("   - Token expirado")
            print("   - Clave secreta diferente")
            print("   - Formato de token incorrecto")
            print(f"📄 Respuesta: {response.text}")
        elif response.status_code == 403:
            print("⚠️ TOKEN VÁLIDO pero PERMISOS INSUFICIENTES")
            print("🔍 El token se validó pero el rol no permite crear convocatorias")
            print("✅ Roles permitidos: 'administrador' o 'profesional'")
            print(f"📄 Respuesta: {response.text}")
        else:
            print(f"❓ RESPUESTA INESPERADA: {response.status_code}")
            print(f"📄 Respuesta: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ ERROR DE CONEXIÓN")
        print("🔍 Verifica que el backend de convocatorias esté ejecutándose en puerto 8008")
    except requests.exceptions.Timeout:
        print("❌ TIMEOUT - El servidor tardó demasiado en responder")
    except Exception as e:
        print(f"❌ ERROR INESPERADO: {e}")
    
    print(f"\n💡 NOTAS:")
    print("- Si obtienes 401, el problema es la configuración JWT")
    print("- Si obtienes 403, el token es válido pero faltan permisos")
    print("- Si obtienes 201, ¡todo funciona perfectamente!")

if __name__ == "__main__":
    test_jwt_compatibility()