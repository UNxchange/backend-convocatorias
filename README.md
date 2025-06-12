# Microservicio Convocatorias - UnxChange

Este microservicio implementa el CRUD de convocatorias de movilidad académica bajo arquitectura SOFEA.

## 🚀 Tecnologías

- Python 3.12
- FastAPI
- MongoDB (NoSQL Documental)
- Motor (Async MongoDB Driver)
- Pydantic
- Dotenv

## 📦 Estructura del Proyecto

- app/main.py → Entrada de la aplicación
- app/models.py → Modelos de datos
- app/database.py → Conexión a MongoDB
- app/routes/convocatorias.py → Endpoints REST

## ⚙ Configuración local

1️⃣ Instalar dependencias y ejecutar el servicio:

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```
