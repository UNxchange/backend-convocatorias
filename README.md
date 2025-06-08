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
- app/db/mongodb.py → Conexión a MongoDB
- app/routes/convocatorias.py → Endpoints REST
- app/services/convocatorias_service.py → Lógica de negocio

## ⚙ Configuración local

1️⃣ Instalar dependencias:

```bash
pip install -r requirements.txt
```
