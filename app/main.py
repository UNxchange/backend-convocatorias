from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import convocatorias
#metrics
from app.metrics import prometheus_middleware, prometheus_metrics

app = FastAPI(
    title="API de Convocatorias UnxChange",
    description="Provee acceso a las convocatorias de movilidad académica.",
    version="1.0.0"
)




# Agregar el middleware
app.middleware("http")(prometheus_middleware)

# Configuración de CORS para permitir que el frontend se conecte
# Para producción, es mejor restringir los orígenes
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # En desarrollo se puede usar "*"
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir las rutas del módulo de convocatorias
app.include_router(convocatorias.router)

@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Bienvenido a la API de Convocatorias UnxChange"}

# Endpoint para Prometheus
@app.get("/metrics")
def metrics():
    return prometheus_metrics()