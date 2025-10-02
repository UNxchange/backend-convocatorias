from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import convocatorias

app = FastAPI(
    title="API de Convocatorias UnxChange",
    description="Provee acceso a las convocatorias de movilidad académica.",
    version="1.0.0"
)

# Configuración de CORS para permitir que el frontend se conecte
# Para producción, es mejor restringir los orígenes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir todos los orígenes en desarrollo
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# Incluir las rutas del módulo de convocatorias
app.include_router(convocatorias.router)

@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Bienvenido a la API de Convocatorias UnxChange"}