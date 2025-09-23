#!/usr/bin/env python3
"""
Script para iniciar el backend de convocatorias con la configuración correcta
"""
import uvicorn
import os
import sys

# Agregar el directorio actual al path de Python
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    print("🚀 Iniciando Backend de Convocatorias UnxChange...")
    print("📍 Puerto: 8008")
    print("🔗 URL: http://localhost:8008")
    print("📚 Documentación: http://localhost:8008/docs")
    print("=" * 50)
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8008,
        reload=False,  # Desactivar recarga automática para mayor estabilidad
        log_level="info"
    )