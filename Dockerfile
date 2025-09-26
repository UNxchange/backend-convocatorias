# Dockerfile robusto para backend-convocatorias
FROM python:3.12-slim

# Configurar variables de entorno para pip
ENV PIP_DEFAULT_TIMEOUT=100
ENV PIP_DISABLE_PIP_VERSION_CHECK=1
ENV PIP_NO_CACHE_DIR=1

# Instalar dependencias del sistema con reintentos
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar el archivo de requisitos
COPY requirements.txt .

# Actualizar pip e instalar dependencias con múltiples estrategias de reintento
RUN pip install --upgrade pip setuptools wheel && \
    pip install --retries 10 --timeout 120 --no-cache-dir -r requirements.txt || \
    (sleep 10 && pip install --retries 5 --timeout 60 --no-cache-dir -r requirements.txt) || \
    (sleep 20 && pip install --no-deps --no-cache-dir -r requirements.txt)

# Copiar el código de la aplicación
COPY . .

# Exponer el puerto
EXPOSE 8002

# Comando para ejecutar la aplicación
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8002"]