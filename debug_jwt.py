#!/usr/bin/env python3
"""
Script para debuggear tokens JWT y configuración de autenticación
"""
import os
from jose import jwt, JWTError
from dotenv import load_dotenv
import json

load_dotenv()

def analyze_token(token_string):
    """Analiza un token JWT sin validar la firma"""
    try:
        # Decodificar sin verificar firma para ver el contenido
        unverified = jwt.get_unverified_header(token_string)
        claims = jwt.get_unverified_claims(token_string)
        
        print("🔍 ANÁLISIS DEL TOKEN:")
        print("=" * 50)
        print(f"📋 Header: {json.dumps(unverified, indent=2)}")
        print(f"📄 Claims: {json.dumps(claims, indent=2)}")
        print(f"📏 Longitud: {len(token_string)} caracteres")
        
        return unverified, claims
    except Exception as e:
        print(f"❌ Error analizando token: {e}")
        return None, None

def test_token_validation(token_string, secret_key, algorithm="HS256"):
    """Prueba validar un token con la clave secreta actual"""
    try:
        print(f"\n🔐 PROBANDO VALIDACIÓN:")
        print("=" * 50)
        print(f"🔑 Secret Key: {secret_key[:20]}...{secret_key[-10:]}")
        print(f"🛡️ Algorithm: {algorithm}")
        
        payload = jwt.decode(token_string, secret_key, algorithms=[algorithm])
        print(f"✅ TOKEN VÁLIDO!")
        print(f"📊 Payload: {json.dumps(payload, indent=2)}")
        return True, payload
    except JWTError as e:
        print(f"❌ TOKEN INVÁLIDO: {e}")
        return False, None

def main():
    print("🧪 DEBUGGER DE TOKENS JWT")
    print("=" * 50)
    
    # Configuración actual
    current_secret = os.getenv("SECRET_KEY")
    current_algorithm = os.getenv("ALGORITHM", "HS256")
    
    print(f"⚙️ CONFIGURACIÓN ACTUAL:")
    print(f"🔑 Secret Key: {current_secret[:20] if current_secret else 'NO ENCONTRADA'}...")
    print(f"🛡️ Algorithm: {current_algorithm}")
    
    # Solicitar token para analizar
    print(f"\n📝 Pega aquí el token JWT que quieres analizar:")
    print("(El token que está funcionando en tu backend de Auth)")
    token = input("Token: ").strip()
    
    if token:
        # Analizar estructura del token
        header, claims = analyze_token(token)
        
        if header and claims:
            # Probar validación con clave actual
            test_token_validation(token, current_secret, current_algorithm)
            
            print(f"\n💡 RECOMENDACIONES:")
            print("=" * 50)
            print("1. Verifica que ambos backends usen la MISMA SECRET_KEY")
            print("2. Asegúrate de que el token contenga los campos 'sub' y 'role'")
            print("3. Confirma que el algoritmo sea HS256 en ambos servicios")
    else:
        print("❌ No se proporcionó token")

if __name__ == "__main__":
    main()