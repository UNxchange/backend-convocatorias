from fastapi import FastAPI
from app.routes import convocatorias
from app.db import mongodb
import asyncio

app = FastAPI(title="Servicio de Convocatorias UnxChange")

# Conexión a la base de datos
@app.on_event("startup")
async def startup_db_client():
    await mongodb.connect()

@app.on_event("shutdown")
async def shutdown_db_client():
    await mongodb.close()

app.include_router(convocatorias.router)